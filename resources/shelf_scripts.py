# activate select facetree tool

try:
	reload(reload_all)
	maya.cmds.deleteUI(facetreeToolContext, toolContext = True);
	maya.cmds.unloadPlugin('paper_model_tools_plugin.py')

except NameError:
	import sys
	if not 'u:/modules/unfolder' in sys.path:
		sys.path.append('u:/modules/')	
	import reload_all

maya.cmds.loadPlugin('u:/modules/paper_model_tools_plugin.py')
facetreeToolContext = maya.cmds.selectFacetree()
maya.cmds.setToolTo(facetreeToolContext)
