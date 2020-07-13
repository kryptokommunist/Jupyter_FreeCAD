import ipywidgets as widgets
from traitlets import Unicode, CFloat, Int, List

@widgets.register
class first_widget(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('FirstView').tag(sync=True)
    _model_name = Unicode('FirstModel').tag(sync=True)
    _view_module = Unicode('first-widget').tag(sync=True)
    _model_module = Unicode('first-widget').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    value = Unicode('Hello World!').tag(sync=True)


import pythreejs

class CubicLattice(pythreejs.Blackbox):
    _model_name: Unicode('CubicLatticeModel').tag(sync=True)
    _model_module = Unicode('first-widget').tag(sync=True)

    basis = List(
        trait=pythreejs.Vector3(),
        default_value=[[0, 0, 0]],
        max_length=5
    ).tag(sync=True)

    repetitions = List(
        trait=Int(),
        default_value=[5, 5, 5],
        min_length=3,
        max_length=3
    ).tag(sync=True)
