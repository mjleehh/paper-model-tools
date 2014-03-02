try:
	maya.cmds.deleteUI(facetreeToolContext, toolContext = True);
	maya.cmds.unloadPlugin('facetree_plugin.py')

	reload(flattenmesh)
	reload(helpers)
	reload(connectedfaces)
	reload(facetree)
	relaod(coordinatesystem)
	reload(patch)
except NameError:
	import sys
	if not 'u:/modules/' in sys.path:
		sys.path.append('u:/modules')

	import flattenmesh
	import helpers
	import connectedfaces
	import facetree
	import coordinatesystem
	import patch

maya.cmds.loadPlugin('u:/modules/facetree_plugin.py')
facetreeToolContext = maya.cmds.selectFacetree()
maya.cmds.setToolTo(facetreeToolContext)
