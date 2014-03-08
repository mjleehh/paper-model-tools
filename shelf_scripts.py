try:
	maya.cmds.deleteUI(facetreeToolContext, toolContext = True);
	maya.cmds.unloadPlugin('facetree_plugin.py')

	reload(flatten_mesh)
	reload(helpers)
	reload(selected_faces)
	reload(facetree)
	relaod(coordinate_system)
	reload(patch)
except NameError:
	import sys
	if not 'u:/modules/' in sys.path:
		sys.path.append('u:/modules')

	import flatten_mesh
	import helpers
	import selected_faces
	import facetree
	import coordinate_system
	import patch

maya.cmds.loadPlugin('u:/modules/facetree_plugin.py')
facetreeToolContext = maya.cmds.selectFacetree()
maya.cmds.setToolTo(facetreeToolContext)
