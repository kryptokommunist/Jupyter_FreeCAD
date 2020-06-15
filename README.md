# FreeCAD inside Jupyter Notebook
## Introduction
### A better IPython and Jupyter Notebook Integration for FreeCAD

Currently, FreeCAD's IPython and Jupyter Notebook integration can only provide visualization by running the entire FreeCAD GUI alongside the notebook. Besides not being elegant it brings many problems with it, like not being able to save the visualizations inside the notebook for sharing or bringing visual complexity of the entire GUI into the view instead of just displaying the 3D model. It is therefore important to find a way to visualize FreeCAD's 3D scene in the IPython display system as supported by Jupyter Notebook.

Tackling the open issue “IPython / Jupyter support” I aim to implement a IPython compatible visualization of FreeCAD’s 3D Open Inventor scene graph. To achieve this I intend to choose a suitable JavaScript library able to render a 3D scene graph and to implement a mapping between it and the Open Inventor scene graph. After this as a byproduct I want to implement a better WebGL export based on the scene graph instead of document objects as currently found in FreeCAD. For this I can reuse and integrate the scene graph mapping component. Lastly I want to document the results in the Wiki and create an example Jupyter notebook.

## How to

Currently tested on Ubuntu 18.04.4 LTS

  - Install FreeCAD daily:
    ```bash
    sudo add-apt-repository ppa:freecad-maintainers/freecad-daily
    sudo apt-get update
    sudo apt-get install freecad-daily
    ``` 
 - Install Jupyter Notebook: `sudo apt install jupyter-notebook`
 - Link external workbench from this repo to FreeCAD (use correct paths for your install): `sudo ln -s /home/kryptokommunist/Documents/Jupyter_FreeCAD/Jupyter/ /usr/shared/freecad-daily/Mod/Jupyter
`- Install pythreejs:
    ```bash
    pip3 install pythreejs
    jupyter nbextension install --py --symlink --sys-prefix pythreejs
    jupyter nbextension enable --py --sys-prefix pythreejs
    ```
 - Start Jupyter Notebook with `jupyter notebook`