# -*- coding: utf-8 -*-

"""
This module contains functions that enable rendering FreeCAD Document objects inside
an IPython environment, for example inside a Jupyter Notebook. The function needed to
do this is `render_document`.
"""

#***************************************************************************
#*   (c) Marcus Ding 2020                                                  *   
#*                                                                         *
#*   This file is part of the FreeCAD CAx development system.              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   FreeCAD is distributed in the hope that it will be useful,            *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        * 
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with FreeCAD; if not, write to the Free Software        * 
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#*   Marcus Ding 2020                                                      *
#***************************************************************************/

import FreeCADGui
from pythreejs import Mesh, Sphere, BufferGeometry, BufferAttribute, MeshPhongMaterial,\
                      LineBasicMaterial, Line, LineSegments, EdgesGeometry, Group, Scene,\
                      Picker, VertexNormalsHelper, PointLight, AmbientLight, PerspectiveCamera,\
                      MeshLambertMaterial, OrbitControls, Renderer
from pivy import coin
import numpy as np
from ipywidgets import HTML
from IPython.display import display, DisplayHandle

from typing import Union, List, Tuple

HIGHLIGHTING_COLOR = (0,1,0)
LINE_WIDTH = 10

# types:

SoVectorType = Tuple[float, float, float]
SoQuaternionType = Tuple[float, float, float, float]
SoCoinTupleType = Tuple[coin.SoIndexedFaceSet, coin.SoCoordinate3, coin.SoMaterial, int, coin.SoTransform]
ThreeJSSceneGraphObjectType = Union[Mesh, Line, Sphere]
ThreeJSSceneGraphObjectListType = List[ThreeJSSceneGraphObjectType]
PartIndicesType = List[List[int]]
SoCoordValsListType = List[SoVectorType]
SoIndicesListType = List[List[int]]

def so_col_to_hex(so_color: tuple) -> str:
    """
    Translate Coin scene object color into html hex color strings.
    >>>so_col_tohex((1,0,0.5))
    "#ff0008"
    """
    color = (int(so_color[0]*255), 
                  int(so_color[1]*255),
                  int(so_color[2]*255))
    hex_col = "#{0:02x}{1:02x}{2:02x}".format(color[0],
                                              color[1],
                                              color[2])
    return hex_col

def transform_indices(so_node: Union[coin.SoIndexedFaceSet, coin.SoIndexedLineSet]) ->  SoIndicesListType:
    """
    Returns list of lists that represent indices from pivy.coin
    scene objects 'SoIndexedLineSet' and 'SoIndexedFaceSet'.
    When ever a -1 is encountered in `so_node.coordIndex` a separate new Line or Face
    is created
    """
    faces_lines = list(so_node.coordIndex)
    indices = []
    curr_line: List[int] = []
    for i in faces_lines:
        if i == -1:
            indices.append(curr_line)
            curr_line = []
            continue
        curr_line.append(i)
    return indices

def generate_line_vertices(line_indices: List[int], coord_vals: SoCoordValsListType) -> SoCoordValsListType:
    """
    Replaces indices in list with the corresponding coordinate values
    """
    line_vertices = []
    for i in line_indices:
        line_vertices.append(coord_vals[i])
    return line_vertices

def extract_values(res_tuple: SoCoinTupleType)\
    -> Tuple[SoCoordValsListType, SoIndicesListType, SoQuaternionType, SoVectorType, SoVectorType, int, bool]:
    """
    Given the Coin3D scene graph object tuple the function will return the information
    (coordinates, indices etc.) in an more basic python type as in the typing specification.
    """
    so_face_line = res_tuple[0] 
    so_coord = res_tuple[1]
    so_shaded_material = res_tuple[2]
    
    coords = list(so_coord.point)
    so_shaded_color = so_shaded_material.diffuseColor.getValues()[0]
    so_shaded_emissive_color = so_shaded_material.emissiveColor.getValues()[0]
    color = (so_shaded_color[0], so_shaded_color[1], so_shaded_color[2])
    emissive_color = (so_shaded_color[0], so_shaded_color[1], so_shaded_color[2])
    transparency = so_shaded_material.transparency[0]
    
    coord_vals = [tuple(x) for x in coords]
    indices = transform_indices(so_face_line)
 
    is_line = False
    if isinstance(so_face_line, coin.SoIndexedLineSet):
        is_line = True
    else:
        if not isinstance(so_face_line, coin.SoIndexedFaceSet):
            raise Exception("Unsupported type of given node: {}".format(type(so_face_line)))
    
    so_transform = res_tuple[4]
    translation = tuple(so_transform.translation.getValue())
    quaternions = tuple(so_transform.rotation.getValue().getValue())

    return coord_vals, indices, quaternions, translation, color, transparency, is_line

def compute_normals(faces: List[Tuple[int, int, int]], vertices: List[SoVectorType]) -> np.array:
    """
    Returns a list of normals for
    each vertex.
    
    Input for N faces
    should be numpy array of shape (N, 3)
    and for M vertices shape (M, 3) respectively
    """
    normals = np.zeros((len(vertices), 3), dtype='float32')
    for face in faces:
        v_index_a = face[0]
        v_index_b = face[1]
        v_index_c = face[2]
        vec_a = vertices[v_index_a]
        vec_b = vertices[v_index_b]
        vec_c = vertices[v_index_c]
        vec_a_b = np.subtract(vec_b, vec_a)
        vec_a_c = np.subtract(vec_c, vec_a)
        dot_p = np.cross(vec_a_b, vec_a_c)
        for i in [v_index_a, v_index_b, v_index_c]:
            np.add(normals[i], dot_p, normals[i])
    return normals

def create_geometry(res_tuple: SoCoinTupleType,
                    name: str="", show_faces: bool=True, show_lines: bool=True) -> ThreeJSSceneGraphObjectListType:
    """Returns PyThreeJS representations of the given Coin3D object tuples."""
    coord_vals, indices, quaternion, translation, color, transparency, is_line = extract_values(res_tuple)
    if is_line and show_lines:
        # geometry based on coin.IndexedLineSet
        geoms = create_line_geom(coord_vals, indices, color, translation, quaternion)
    elif not is_line and show_faces:
        # geometry based on coin.IndexedFaceSet
        geoms = create_face_geom(coord_vals, indices, color, transparency, translation, quaternion)
    else:
        return []
    if name:
        for obj in geoms:
            obj.freecad_name = name
    return geoms

def create_face_geom(coord_vals: SoCoordValsListType,
                     face_indices: SoIndicesListType, 
                     face_color: SoVectorType,
                     transparency: float,
                     translation: SoVectorType=None,
                     quaternion: SoQuaternionType=None) -> ThreeJSSceneGraphObjectListType:
    """
    Returns a pythreejs `Mesh` object that consists of the faces given by
    face_indices and the coord_vals.
    
    Additionally the attributes `Mesh.default_material` and `Mesh.geometry.default_color`
    will be set before returning the Mesh. Those attributes contain references to the
    default colors and materials that are set in this function to restore later changes.
    """
    vertices = np.asarray(coord_vals, dtype='float32')
    faces = np.asarray(face_indices, dtype='uint16')

    normals = compute_normals(faces, vertices)
        
    faces = faces.ravel()
    vertexcolors = np.asarray([face_color]*len(coord_vals), dtype='float32')


    face_geometry = BufferGeometry(attributes=dict(
        position=BufferAttribute(vertices, normalized=False),
        index=BufferAttribute(faces, normalized=False),
        normal=BufferAttribute(normals, normalized=False),
        color=BufferAttribute(vertexcolors, normalized=False)
    ))
    # this is used for returning to original state after highlighting
    face_geometry.default_color = vertexcolors 
    
    # BUG: This is a bug in pythreejs and currently does not work
    #faceGeometry.exec_three_obj_method('computeFaceNormals')
    #faceGeometry.exec_three_obj_method('computeVertexNormals')
    col = so_col_to_hex(face_color)
    material = MeshPhongMaterial(color=col, transparency=transparency,depthTest=True, depthWrite=True, metalness=0)
    object_mesh = Mesh(
        geometry=face_geometry,
        material=material,
        position=[0,0,0]   # Center the cube
    )
    object_mesh.default_material = material
    
    if quaternion:
        object_mesh.quaternion = quaternion
    if translation:
        object_mesh.position = translation
    return [object_mesh]

def create_line_geom(coord_vals: SoCoordValsListType,
                     indices: SoIndicesListType,
                     line_color: SoVectorType,
                     translation: SoVectorType=None,
                     quaternion: SoQuaternionType=None) -> ThreeJSSceneGraphObjectListType:
    """
    Return a pythreejs Line object consisting of lines
    defined by the line_indices and the coord_vals.
    
    Additionally the attributes `Line.default_color` and `Line.edge_index`
    will be set before returning the `Line` array. Those attributes contain references to the
    default colors, that are set in this function to restore later changes, and the FreeCAD edge index.
    """
    lines = []
    for i, line_indices in enumerate(indices):
        vertices = generate_line_vertices(line_indices, coord_vals)
        vertices = np.array(vertices, dtype="float32")
        line_geom = BufferGeometry(attributes=dict(
        position=BufferAttribute(vertices, normalized=False)))
        # BUG: This is a bug in pythreejs and currently does not work
        #linesgeom.exec_three_obj_method('computeVertexNormals')
        col = so_col_to_hex(line_color)
        material = LineBasicMaterial(linewidth=LINE_WIDTH, color=col)
        material.default_color = col        
        line = Line(geometry=line_geom, 
                     material=material)
        line.edge_index = i + 1 # using FreeCAD's 1-based indexing
        if translation:
            line.position = translation
        if quaternion:
            line.quaternion = quaternion
        lines.append(line)
    return lines

def bfs_traversal(node: coin.SoNode,
                  coordinates: Union[coin.SoCoordinate3, None]=None,
                  material: Union[coin.SoMaterial, None]=None,
                  transform: Union[coin.SoTransform, None]=None, 
                  index: int=0,
                  print_tree: bool=False,
                  depth_counter: int=0,
                  object_index: int=0) -> List[SoCoinTupleType]:
    """
    Return list of all (SoIndexed(Line/Face)Set, SoCoordinate3, SoMaterial) tuples
    inside the scene graph.
    
    The breadth first search always referes to the parent material and coordinates
    if there aren't any on the same level.
    """
    if print_tree:
        print(str("   " * index) + str(type(node)))
    if not isinstance(node, (coin.SoSwitch, coin.SoSeparator)):
        return []
    coords = coordinates
    mat = material
    trans = transform
    edge_face_set = None
    for child in node:
        if isinstance(child, coin.SoCoordinate3):
            coords = child
        if isinstance(child, coin.SoTransform):
            trans = child
        if isinstance(child, coin.SoMaterial):
            mat = child
        if isinstance(child, (coin.SoIndexedLineSet, coin.SoIndexedFaceSet)):
            edge_face_set = child
    res_children = []
    this_object_index = -1
    for child in node:
        if depth_counter != 0:
            this_object_index = object_index
        else:
            this_object_index += 1
        res_recursive = bfs_traversal(child, coords, transform=trans, index=index+1,\
                                      print_tree=print_tree, depth_counter=depth_counter+1,\
                                      object_index=this_object_index)
        res_children.extend(res_recursive)
    if edge_face_set:
        res = [(edge_face_set, coords, mat, this_object_index, trans)]
    else:
        res = []
    res.extend(res_children)
    return res

def get_line_geometries(geometries: Group) -> LineSegments:
    """
    Return line segments that represent the edges of the given objects mesh.
    """
    new_geometries = Group()
    for geom in list(geometries.children):
        line_geom = EdgesGeometry(geom.geometry)
        lines = LineSegments(geometry=line_geom, 
                 material=LineBasicMaterial(linewidth=5, color='#000000'))
        new_geometries.add(lines)
    return new_geometries

def get_name(obj: Union[ThreeJSSceneGraphObjectType, None]) -> str:
    """
    Returns `object.name` except if `object is None`.
    Then returns string `"None"`.
    """
    if obj is None:
        return "None"
    return obj.name

def part_index_by_name(name: str, part_indices: PartIndicesType) -> List[int]:
    """
    Returns `coin.IndexedFaceSet`s `partIndex` attribute given the
    pythreejs Geometry `name` attribute containing the objects index in the 
    Coin scene graph at the beginning of the name.
    >>part_index_by_name("2 4", [[1,1,1], [2,3,4], [222]])
    [222]
    """
    part_index_str = name.split()[0]
    part_index = int(part_index_str)
    return part_indices[part_index]
    
def index_by_face_index(part_index: List[int], face_index: int) -> Union[int, None]:
    """
    Returns the index of the Shape face for a given face index.
    If the face index is not in the part_index returns `None`.
    """
    upper_limit = 0
    for i, part_num_elements in enumerate(part_index):
        upper_limit += part_num_elements
        if face_index < upper_limit:
            return i + 1 # FreeCAD uses 1-based indexing
    return None

def vertices_col_highlight_face(shape_face_index: int,
                                cols_default: np.array,
                                part_index: List[int],
                                face_indices: List[int]) -> np.array :
    """
    Returns vertex color array where the indexed face is highlighted.
    """
    cols = np.copy(cols_default)
    start_index = 0
    for i in range(shape_face_index-1): #this is using the freecad base 1-indexing!
        start_index += part_index[i]*3
    end_index = start_index + part_index[shape_face_index-1]*3 - 1
    if start_index < 0:
        start_index = 0
    for i in range(start_index, end_index+1):
        pos_index = face_indices[i]
        cols[pos_index] = HIGHLIGHTING_COLOR
    return cols

def reset_object_highlighting(obj: ThreeJSSceneGraphObjectType) -> None:
    """
    After calling this function the object of type `Line`, `Sphere` or `Mesh` will be reset
    to it's default colors.
    """
    # case obj is a Line
    if isinstance(obj, Line):
        obj.material.color = obj.material.default_color
        return
    
    # case obj is a Sphere (representing a vertex)
    if isinstance(obj, Sphere):
        # TODO
        return
    
    # case obj is a Mesh of faces
    obj.material = obj.default_material
    obj.geometry.attributes["color"].array = obj.geometry.default_color
    obj.geometry.attributes["color"].needsUpdate = True        
    
def freecad_name_from_obj3d(obj3d: ThreeJSSceneGraphObjectType) -> str:
    """
    Returns the objects name inside the FreeCAD document.
    """
    txt = ""
    if hasattr(obj3d, "freecad_name"):
        txt = "{}: ".format(obj3d.freecad_name)
    return txt
    
def generate_picker(geometries: ThreeJSSceneGraphObjectListType,
                    part_indices: PartIndicesType,
                    mode: str="click") -> Tuple[HTML, Picker]:
    """
    Returns a picker that will enable object and face selection
    as well as highlighting those selections
    
    Picker mode can be `mousemove` or `click` or `dblclick` and is set via the `mode`
    parameter.
    """
    VALUE_TYPE = "point"
    VALID_MODES = ["mousemove", "click", "dblclick"]
    
    if mode not in VALID_MODES:
        raise Exception("Given `mode` parameter has to be on of {}, but was `{}`"
                        .format(VALID_MODES, mode))
    html = HTML("<b>No selection.</b>")
    picker = Picker(
        controlling = geometries,
        event = mode)
    picker.shape_face_index_old = -1
    picker.last_object = None
    
    def callback_f(change):
        """
        This functions implements highlighting and displaying the name 
        of selected faces and edges as well as vertices. You seemingly can't
        select nothing, it only triggers on objects.
        """
        value = picker.object
        value_freecad_name = freecad_name_from_obj3d(value)
        last_value = picker.last_object

        if value is None:
            if not (last_value is None):
                reset_object_highlighting(last_value)
            html.value = "<b>No selection.</b>"
            return
        
        if isinstance(value, Line):
            if not (last_value is None):
                reset_object_highlighting(last_value)
            value.material.color = so_col_to_hex(HIGHLIGHTING_COLOR)
            html.value = "{} <b>Edge{}</b>".format(value_freecad_name, value.edge_index)
            return

        face_index = int(picker.faceIndex)
        part_index = part_index_by_name(get_name(value), part_indices)
        shape_face_index = index_by_face_index(part_index, face_index)        

        if not (last_value is None):
            # check for case of selecting the same freecad face
            if (last_value.name == value.name) and (picker.shape_face_index_old == shape_face_index):
                return
            reset_object_highlighting(last_value)

        face_indices = value.geometry.attributes["index"].array
        cols_default = value.geometry.default_color
        cols_highlighted = vertices_col_highlight_face(shape_face_index, cols_default, part_index, face_indices)
        value.geometry.attributes["color"].array = cols_highlighted
        value.geometry.attributes["color"].needsUpdate = True 
        
        material = MeshLambertMaterial(vertexColors='VertexColors', shininess=1)
        material.name = value.material.color
        value.material = material
        picker.shape_face_index_old = shape_face_index
        picker.last_object = value

        html.value = "{} <b>Face{}</b>".format(value_freecad_name, shape_face_index)

    picker.observe(callback_f, names=[VALUE_TYPE]) 
    return html, picker

# TODO : Add displaying the FreeCAD object names to the renderer
def render_objects(root_node: coin.SoSeparator,
                   names: List[str]=[],
                   show_line_geom: bool=False,
                   show_normals: bool=False,
                   selection_mode: Union[str, None]="mousemove") -> DisplayHandle:
    """
    Renders any coin node containing LineSets or FaceSets.
    
    show_line_geom: Just display the Mesh.
    show_normals: Display the vertex normals.
    """
    view_width = 600
    view_height = 600
    geometries = Group()
    part_indices = [] # contains the partIndex indices that relate triangle faces to shape faces
    render_face_set = True
    i = 0
    for res in bfs_traversal(root_node, print_tree=False):
        if isinstance(res[0], coin.SoIndexedFaceSet) and render_face_set:
            render_face_set = False
            continue
        if isinstance(res[0], coin.SoIndexedFaceSet):
            render_face_set = True
            part_index_list = list(res[0].partIndex)
            part_indices.append(part_index_list)
        else:
            continue
        
        geoms = create_geometry(res)
        
        for obj3d in geoms:
            obj3d.name = str(res[3]) + " " + str(i) #the name of the object is `object_index i`
            i += 1
        
        if geoms and show_normals:
            helper = VertexNormalsHelper(geom[0])
            geoms.append(helper)
        
        for geom in geoms:
            geometries.add(geom)
    
    if show_line_geom:
        geometries = get_line_geometries(geometries)
        
    light = PointLight(color="white", position=[40,40,40], intensity=1.0, castShadow=True)
    ambient_light = AmbientLight(intensity=0.5)
    camera = PerspectiveCamera(
        position=[0, -40, 20], fov=40,
        aspect=view_width/view_height)
    children = [camera, light, ambient_light]
    children.append(geometries)
    scene = Scene(children=children)
    scene.background = "#65659a"
 
    controls = [OrbitControls(controlling=camera)]
    html = HTML()

    if selection_mode:
        html, picker = generate_picker(geometries, part_indices, "mousemove")
        controls.append(picker)
    
    renderer = Renderer(camera=camera,
                    scene=scene, controls=controls,
                    width=view_width, height=view_height)
    return display(renderer, html)

# TODO : Add typing after finding out how to reference the document class
def document_to_scene_graph(doc) -> Tuple[coin.SoSeparator, List[str]]:
    """Convert a FreeCAD document to a Coin3D scene graph and retain a list of object names"""
    root = coin.SoSeparator()
    names = []
    for obj in doc.Objects:
        root.addChild(FreeCADGui.subgraphFromObject(obj))
        names.append(obj.Name)
    return root, names

# TODO : Add typing after finding out how to reference the document class
def render_document(doc) -> DisplayHandle:
    """Display a FreeCAD document inside an IPython environment, e.g. Jupyter Notebook"""
    root, names = document_to_scene_graph(doc)
    return render_objects(root, names)
