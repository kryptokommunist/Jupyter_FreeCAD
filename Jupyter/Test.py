from IPython.display import display, display_html
from pythreejs import *
import ipywidgets


def test():
    print("test")

def display_js_example():
    # Reduce repo churn for examples with embedded state:
    from pythreejs._example_helper import use_example_model_ids
    use_example_model_ids()

    view_width = 600
    view_height = 400

    sphere = Mesh(
        SphereBufferGeometry(1, 32, 16),
        MeshStandardMaterial(color='red')
    )

    cube = Mesh(
        BoxBufferGeometry(1, 1, 1),
        MeshPhysicalMaterial(color='green'),
        position=[2, 0, 4]
    )

    camera = PerspectiveCamera(position=[10, 6, 10],
                               aspect=view_width / view_height)
    key_light = DirectionalLight(position=[0, 10, 10])
    ambient_light = AmbientLight()

    positon_track = VectorKeyframeTrack(name='.position',
                                        times=[0, 2, 5],
                                        values=[10, 6, 10,
                                                6.3, 3.78, 6.3,
                                                -2.98, 0.84, 9.2,
                                                ])
    rotation_track = QuaternionKeyframeTrack(name='.quaternion',
                                             times=[0, 2, 5],
                                             values=[-0.184, 0.375, 0.0762,
                                                     0.905,
                                                     -0.184, 0.375, 0.0762,
                                                     0.905,
                                                     -0.0430, -0.156, -0.00681,
                                                     0.987,
                                                     ])

    camera_clip = AnimationClip(tracks=[positon_track, rotation_track])
    camera_action = AnimationAction(AnimationMixer(camera), camera_clip, camera)

    scene = Scene(children=[sphere, cube, camera, key_light, ambient_light])
    controller = OrbitControls(controlling=camera)
    renderer = Renderer(camera=camera, scene=scene, controls=[controller],
                        width=view_width, height=view_height)
    return renderer