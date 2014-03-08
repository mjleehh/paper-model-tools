from unfolder import unfold_command
from unfolder.automatic_unfold import selected_faces
from unfolder.create_patch import patch
from unfolder.util import plane_coordinate_system, helpers

try:
	maya.cmds.deleteUI(facetreeToolContext, toolContext = True);
	maya.cmds.unloadPlugin('unfold_tool.py')

	reload(unfold_command)
	reload(helpers)
	reload(selected_faces)
	reload(unfolder)
	relaod(plane_coordinate_system)
	reload(patch)
except NameError:
	import sys
	if not 'u:/modules/' in sys.path:
		sys.path.append('u:/modules')
import unfolder

maya.cmds.loadPlugin('u:/modules/unfold_tool.py')
facetreeToolContext = maya.cmds.selectFacetree()
maya.cmds.setToolTo(facetreeToolContext)
