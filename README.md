Paper Model Tools
=================

The Paper Model Tools is a set of tools to create 2D paper model sheets from 3D
mesh geometry. They are currently implemented as a plugin for Autodesk Maya.

![showcase](https://raw.github.com/mjleehh/paper-model-tools/master/doc/images/showcase.png)

Two objects and paper models of these objects that were created using the Paper
Model Tools.

Installation
------------

Currently there are no packaged release versions of the plugin available for
download. To install the tools download the contents of this repo from

https://github.com/mjleehh/paper-model-tools

and unpack it to a folder of your choice.

In maya go to `Window -> Settings/Preferences -> Plug-in Manager`. In the
Plug-in manager click the `Browse` button and from the Paper Model Tools folder
pick

`paper_model_tools_plugin.py`

Now at the bottom of the list you should see

![loaded plugin in plug-in browser](https://raw.github.com/mjleehh/paper-model-tools/master/doc/images/plugin_loaded.png)

If you wish to load the plugin on startup check the `Auto load` box.

Create Paper Model Tool
-----------------------

This interactive tool lets the user create a paper model from a mesh geometry
controlling the layout of that paper model.

Create Paper Model Command
--------------------------

This tool given a selected mesh object or a set of mesh faces generates a paper
model for that selection.

Copyright and License
---------------------

Paper Model Tools is released under the [GPL V3](http://choosealicense.com/licenses/gpl-v3/).