from .__meta__ import __version__

from .example import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'first-widget',
        'require': 'first-widget/extension'
    }]
