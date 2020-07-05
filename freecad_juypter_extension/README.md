# first-widget

## Introduction

This is a simple widget inspired by the jupyter [doc](https://ipywidgets.readthedocs.io/en/stable/) built using the widget [cookiecutter](https://github.com/jupyter-widgets/widget-cookiecutter).  

This simple widget may serve as an example of working widget with good practices.

To get a feel of the result check out the [demo notebook](https://github.com/ocoudray/first-widget/blob/master/notebooks/demo.ipynb) or the binder link, which takes you through the steps of building your own custom widget: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/PierreMarion23/jupyter-widget-hello-world-binder/master?filepath=hello_world.ipynb).  
Read on for technical details.  

This documentation is based on the work of [oscar6echo](https://gitlab.com/oscar6echo/jupyter-widget-d3-slider/blob/master/README.md) who has contributed heavily to this project.

## 1 - Installation

To install use pip and npm:

    $ git clone https://github.com//First_Custom_Widget.git
    $ cd First_Custom_Widget/js
    $ npm install
    $ cd ..
    $ pip install .


For a development installation:

    $ git clone https://github.com//First_Custom_Widget.git
    $ cd First_Custom_Widget/js
    $ npm install
    $ cd ..
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix first_widget
    $ jupyter nbextension enable --py --sys-prefix first_widget

## 2 - Paths

All the paths directly from a macOS system (with [Anaconda](https://www.anaconda.com/what-is-anaconda/) installed with [brew](https://brew.sh/)) where sys.prefix = `/usr/local/anaconda3`.  
It should be relatively easy to translate in other systems.  


To check where jupyter install extensions:

    $ jupyter --paths
    config:
        /Users/Olivier/.jupyter
        /usr/local/anaconda3/etc/jupyter
        /usr/local/etc/jupyter
        /etc/jupyter
    data:
        /Users/Olivier/Library/Jupyter
        /usr/local/anaconda3/share/jupyter
        /usr/local/share/jupyter
        /usr/share/jupyter
    runtime:
        /Users/Olivier/Library/Jupyter/runtime

The flag `--sys-prefix` means extension are installed in this data folder:

    /usr/local/anaconda3/share/jupyter

There you can see a `first-widget` folder or symlink back to the source folder `static/`.  
For example:

    drwxr-xr-x  4 Olivier  staff   136B Sep 30 18:09 jupyter-js-widgets/
    drwxr-xr-x  5 Olivier  staff   170B Oct  3 02:42 first-widget/

To check nbextensions are properly install and enabled, for example:

    $ jupyter nbextension list
    Known nbextensions:
    config dir: /Users/Olivier/.jupyter/nbconfig
        notebook section
        codefolding/main  enabled 
        - Validating: OK
        comment-uncomment/main  enabled 
        - Validating: OK
        default_style/main  enabled 
        - Validating: OK
    config dir: /usr/local/anaconda3/etc/jupyter/nbconfig
        notebook section
        jupyter-js-widgets/extension  enabled 
        - Validating: OK
        first-widget/extension  enabled 
        - Validating: OK


## 3 - Commands

### 3.1 - `npm install`

It is run from folder `js/` which contains the js+css **source code**.  
It performs the following:
+ Download the node modules mentioned in fields `dependencies` and `devDependencies` in npm config file `package.json`.
+ Run `webpack` according to config file `webpack.config.js`

The first step is the `npm install` command per se.  
The second is the `prepare` command as defined in `package.json`. And `npm prepare` is automatically executed after npm install as explained in the [official doc](https://docs.npmjs.com/misc/scripts).

The result is the creation of folders `js/dist` and `first_widget/static` containing compiled javascript from source code in folder `js/`.

### 3.2 - `pip install`

The full command is:
```bash
# regular install from folder containing setup.py
$ pip install .

# dev install from folder containing setup.py
$ pip install -e .
```

This command must be run **AFTER** the folder `static/` was created.

It is a standard `pip install` command:
+ The source files and egg-info are copied to `/usr/local/anaconda3/lib/python3.6/site-packages`
+ The files in folder `static/` are copied to `share/jupyter/nbextensions/first-widget`
+ the `enable_first_widget.json` file is copied to `etc/jupyter/nbconfig/notebook.d` (see section 3.4)
+ Note that for a **dev install**:
    + An `egg-link` file links back to the source folder
    + No file is copied to the folder `nbextensions/first-widget` and `nbconfig/notebook.d`
    + Thanks to the `--symlink`, during dev, you just need to restart the kernel to take into account any modification in the Python code!

### 3.3 - `jupyter nbextension (install|uninstall)`

This command is now only needed for an install in dev mode, not in normal mode.

The full command is:
```bash
$ jupyter nbextension (install|uninstall) --py [--symlink] --sys-prefix first_widget
```

It copies [create symlinks] resp. removes `static/` files to resp. from the nbextension data folder `share/jupyter/nbextensions/first-widget` and adds resp. removes lines in config file `notebook.json` in config directory `/usr/local/anaconda3/etc/jupyter`.

The config file `notebook.json` contains the following:

    {
        "load_extensions": {
            "jupyter-js-widgets/extension": true,
            "first-widget/extension": true
        }
    }


### 3.4 - `jupyter nbextension (enable|disable)`

This command is now only needed for an install in dev mode, not in normal mode. In normal mode, jupyter notebook extensions are automatically enabled since notebook version 5.3. Automatic enabling works by putting the `enable_first_widget.json` fie in the `etc/jupyter/nbconfig/notebook.d` folder.

The full command is:
```bash
$ jupyter nbextension (enable|disable) --py --sys-prefix first_widget
```

It sets to true resp. false the `first-widget/extension` line in config file `notebook.json` in config directory `/usr/local/anaconda3/etc/jupyter`.

### 3.5 - `npm run prepare`

The full command is:
```bash
# from folder js/
$ npm run prepare
```
It is a script (which simply calls `webpack`) in npm config file `package.json`.  

In an active dev activity (in the folder `js/`) substitute `npm install` by `npm run prepare` as there is no need to reload node_modules from the internet or even to get them from the local npm cache (located in `~/.npm`)

This re-compile the source js folder into `static/`. The symlinks bring back from `share/jupyter/nbextensions/first-widget` to `js/static/`. So just reload the notebook. The new js is available instantly !

### 3.6 - `npm run watch`

To automate the build (i.e. running webpack) process start `npm run watch`.  
It will run in the background and trigger `npm run prepare` each time any change occurs in the `js/lib/` folder.

## 4 - Publish on PyPI and NPM

### 4.1 - Publish new version of first_widget on PyPI

Short version:

```bash
# Update version in __meta__.py
# git add and commit and push

# from top folder 
# see more comments below
python setup.py sdist upload -r pypi

# tag version
git tag -a X.X.X -m 'comment'
git push --tags
```

Long version (about the upload in itself):

A few comments on the release process are available in the RELEASE.md file, created by the cookiecutter. Below is our experience on the matter of publishing on PyPI:

In order to publish a first version of your widget on PyPI:
+ Create an account on [PyPI](https://pypi.python.org/pypi?%3Aaction=register_form)
+ `pip install twine` (if not already installed)
+ `python setup.py sdist`
+ `twine upload dist/*`

To upload a new version of your widget:
+ change version in `first_widget/_version.py`
+ delete `dist`
+ `python setup.py sdist`
+ `twine upload dist/*`

A quicker way to do the same by combining all the steps is: 

`python setup.py sdist upload -r pypi`

The full documentation can be found [here](https://packaging.python.org/tutorials/distributing-packages/).


### 4.2 - Publish new version of first-widget on NPM

In addition to a regular Python packages, the JS part can be published too.  
This is useful only to use jupyter-widgets in a non-notebook context, including in Jupyter Lab.

```bash
# from js/ folder

# clean out the dist/ and node_modules/ folders
# for example to remove any git untracked file/folder: 
# git clean -fdx

# Update version in package.json

npm install

# test run to see what you will publish
# npm pack

# before publishing
# create a user if necessary 
# login npm
# ref: https://docs.npmjs.com/getting-started/publishing-npm-packages

npm publish

# check out the result on https://www.npmjs.com/
```  

## 5 - Publish on conda-forge

### 5.1 - Why conda?

Conda has several advantages over pip:

+ It can handle any dependency: Python packages as well as other libraries - fundamentally it is language agnostic
+ It allows to install binary code, thus paving the way for adding compiled C++ in your package, for instance
+ Like pip it allows to create virtual environments to isolate your projects
+ It allows a one-line install command - no need to manually enable the nbextensions (temporary advantage: see previous section)

Conda packages are available on different channels. The default channel is administrated by Continuum Analytics. The usual recommended channel to upload open source projects is conda-forge, as [this article](https://www.anaconda.com/blog/developer-blog/anaconda-build-migration-conda-forge/) from Anaconda announces. To add this channel to your conda configuration, run the following command:

```bash
conda config --add channels conda-forge
```

To create a conda package, you need to write a recipe describing how to build the package along with the dependencies required for building and running it. The [conda doc](https://conda.io/docs/user-guide/tasks/build-packages/recipe.html) gives the general structure of a recipe, and the way conda builds packages.

### 5.2 - Make your recipe

The main file of the recipe is a `meta.yaml` file. It contains most of the information necessary to build the package:
+ name and version of the package (`package` section)
+ reference to the source code of your package (`source` section)
+ build script (`build` section)
+ dependencies (`requirements` section)
+ tests to perform after building the package (`test` section)
+ additional information (`about` and `extra` sections). 

Conda-forge provides a [template](https://github.com/conda-forge/staged-recipes/blob/master/recipes/example/meta.yaml) for this file. If you want to publish on conda-forge, it is recommended to follow it closely. Be sure to:
+ use a Tarball in `source` section. You will have to include `sha256` as the checksum (you can follow [these instructions](https://conda-forge.org/docs/meta.html#populating-the-hash-field)), even though md5 is provided on PyPI.
+ fill in the `about` and `extra` sections (although they are optional)

In the case of Jupyter widgets the `meta.yaml` file is not enough, as it does not include the nbextensions enable/disable command. To perform this extra step, you must add post-link and pre-unlink files. For example, the [bqplot recipe](https://github.com/conda-forge/bqplot-feedstock/tree/master/recipe) contains the files to be added to the recipe. Of course, change the widget name in all files.

### 5.3 - Test your recipe

In order to test your recipe locally you may follow these steps:
+ `conda install conda-build` installs conda-build which is a specific conda package insofar as it can only be installed in the root environment.
+ `conda-build my_recipe_directory`. At this point, conda builds your package. It will create a folder named `conda-bld` in your root conda folder if all goes well. Inside this folder 2 folders are important:
    + a folder whose name begins by the name of your package. It contained the temporary files created by conda during the build of the package. If the build was successful, the folder should be nearly empty. Else it will contain some remnants of the build process;
    + a folder corresponding to your operating system, which contains a tar archive of the built package.
+ `conda install my_package --use-local` will install the package locally so you can test it.

### 5.4 - Publish on conda-forge

The mechanism to publish on conda-forge is well described in their [user guide](https://conda-forge.org/docs/recipe.html). Following the step-by-step instructions you will have to:
+ fork the [staged recipes](https://github.com/conda-forge/staged-recipes)
+ upload your recipe in your forked staged-recipe repo
+ Open a pull request
+ Check that your recipe successfully passes the automatic tests done by Continuous Integration tools (CircleCI, AppVeyor, Travis CI for respectively Linux, Window, macOS)
+ Wait for a conda-forge admin to merge your pull request - typically within one week

Before opening the pull request, it is highly recommended to make sure that your recipe works at least on your development computer, and if possible on all three operating systems, to avoid cluttering the CI tools with a disfunctional recipe.

### 5.5 - Update your package

If you want to update your recipe, it is recommended to follow [these instructions](https://conda-forge.org/#contribute). Instead of pushing directly your new recipe, it is advised to fork the corresponding repo, edit it and open a pull request. This will automatically launch the building tests. Thus, if your new recipe doesn't pass the tests, the old version remains available. If tests are passed, you will be able to merge the pull request. When built and uploaded on conda-forge, the new version will be available.
