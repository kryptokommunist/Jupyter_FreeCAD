# first-widget

## Introduction

This widget is build on the example widget over at https://github.com//First_Custom_Widget. The full README can be found there.

## 1 - Installation

To install use pip and npm:

    $ cd freecad_juypter_extension
    $ cd js
    $ npm install
    $ cd ..
    $ pip install .

For a development installation:

    $ cd freecad_juypter_extension
    $ cd js
    $ npm install
    $ cd ..
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix first_widget
    $ jupyter nbextension enable --py --sys-prefix first_widget
