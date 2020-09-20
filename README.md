# FreeCAD inside Jupyter Notebook

[![Documentation Status](https://readthedocs.org/projects/ipythonfreecadviewer/badge/?version=latest)](https://ipythonfreecadviewer.readthedocs.io/en/latest/?badge=latest) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/6b9ea8e8c1df41f5a712ccf22974c39c)](https://www.codacy.com/manual/kryptokommunist/Jupyter_FreeCAD?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kryptokommunist/Jupyter_FreeCAD&amp;utm_campaign=Badge_Grade) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/kryptokommunist/Jupyter_FreeCAD.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/kryptokommunist/Jupyter_FreeCAD/context:python)
[![Build Status](https://travis-ci.org/kryptokommunist/Jupyter_FreeCAD.svg?branch=master)](https://travis-ci.org/kryptokommunist/Jupyter_FreeCAD)

## Introduction
### A better IPython and Jupyter Notebook Integration for FreeCAD

Currently, FreeCAD's IPython and Jupyter Notebook integration can only provide visualization by running the entire FreeCAD GUI alongside the notebook. Besides not being elegant it brings many problems with it, like not being able to save the visualizations inside the notebook for sharing or bringing visual complexity of the entire GUI into the view instead of just displaying the 3D model. It is therefore important to find a way to visualize FreeCAD's 3D scene in the IPython display system as supported by Jupyter Notebook.

Tackling the open issue “IPython / Jupyter support” I aim to implement a IPython compatible visualization of FreeCAD’s 3D Open Inventor scene graph. To achieve this I intend to choose a suitable JavaScript library able to render a 3D scene graph and to implement a mapping between it and the Open Inventor scene graph. After this as a byproduct I want to implement a better WebGL export based on the scene graph instead of document objects as currently found in FreeCAD. For this I can reuse and integrate the scene graph mapping component. Lastly I want to document the results in the Wiki and create an example Jupyter notebook.

This project is part of [Google Summer of Code 2020](https://summerofcode.withgoogle.com/projects/#6095514577141760) and the corresponding thread in the FreeCAD forum can be found [here](https://forum.freecadweb.org/viewtopic.php?f=8&t=46039). I wrote a blog post about the project [here](https://kryptokommun.ist/tech/2020/08/31/google-summer-of-code.html). My full project proposal can be found [here](https://docs.google.com/document/d/1VgfsD06Qvb87S-tQazfTsyYTp14Z3EjF4V9puPVNCTQ/edit).

### Demo

Check out [this static demo notebook](https://kryptokommun.ist/google-summer-of-code-2020), it gives an idea about the functionality even though selection and other interactivity is missing.

![FreeCAD rendering inside the notebook demo](https://github.com/kryptokommunist/kryptokommunist.github.io/raw/master/images/gsoc-2020-interactivity-demo.gif)

### Current state

The `freecadviewer` module was only tested with basic shapes from the `Part` workbench so far. It's something to build on. There are some open problems for which I didn't have time before the GSoC deadline (see `TODO` in source):

- highlighting of edges does not work (reason unclear, I couldn't find the error)
- displaying the object names
- showing vertices
- typing the document object
- fixed light source instead of the lightsource moving with rotation
- problem with mocking modules in the documentation, the mock objects show up on the generated page: [example](https://ipythonfreecadviewer.readthedocs.io/en/latest/freecadviewer.html)
 
### Future work

- expanding the viewer to more FreeCAD workbenches with different scene graph structure
- more advanced rotation and navigation
- implementing the so much functionality in Javascript that selection will work on a static page

## How to

### Local install

Currently tested on Ubuntu 18.04.4 LTS and Debian 10 aka Buster.

- Install FreeCAD, e.g. the daily build:
   ```
   sudo add-apt-repository ppa:freecad-maintainers/freecad-daily
   sudo apt-get update
   sudo apt-get install freecad-daily
   ``` 
- Install Jupyter Notebook: `sudo apt install jupyter-notebook`
- Clone this repository: `git clone git@github.com:kryptokommunist/Jupyter_FreeCAD.git`
- Link external workbench from this repo to FreeCAD (use correct paths for your install): 
  ```
  sudo ln -s /home/kryptokommunist/Documents/Jupyter_FreeCAD/Jupyter/ /usr/shared/freecad-daily/Mod/Jupyter
  ```
- Change working directory to this folder and install requirements:
  ```
  pip3 install -r requirements.txt
  ```
- Install pythreejs to the notebook:
  ```
  jupyter nbextension install --py --symlink --sys-prefix pythreejs
  jupyter nbextension enable --py --sys-prefix pythreejs    
  ```
- Start Jupyter Notebook with `jupyter notebook`
- Check if you can render the [example notebook](https://github.com/kryptokommunist/Jupyter_FreeCAD/blob/master/FreeCAD%20inside%20Jupyter%20Notebook%20-%20Examples.ipynb). It should look somewhat like [this](https://kryptokommun.ist/google-summer-of-code-2020).
 
### Development
 
 The relevant file can be found at [IPythonFreeCADViewer/freecadviewer.py](blob/master/IPythonFreeCADViewer/freecadviewer.py). Tools used for development are `pylint` for linting and `mypy` for static type checking. It can be useful to run the code inside the notebook first for faster development iterations.
 
 I will continue to improve the project in the future. You can find the repository [here](https://github.com/kryptokommunist/Jupyter_FreeCAD). If you use the module and encounter any issues or just find it useful, don't hesitate to post to the [forum thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=46039) or let me know with a [tweet](https://twitter.com/kryptokommunist) or an issue in the [repository](https://github.com/kryptokommunist/Jupyter_FreeCAD).

Thanks to my mentors [@ickby](https://forum.freecadweb.org/memberlist.php?mode=viewprofile&u=686), [@kkremitzki](https://twitter.com/thekurtwk), [@yorik](https://twitter.com/yorikvanhavre) and the entire FreeCAD community for running such an awesome project. Thanks to  [@fluepke](https://twitter.com/fluepke) for hosting the development server.

#### Documentation

An API documentation is hosted on [readthedocs](https://ipythonfreecadviewer.readthedocs.io/en/latest/readme.html).
