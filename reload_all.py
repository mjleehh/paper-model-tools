print('reloading')

# top level
import unfolder
reload(unfolder)

# first level
import unfolder.facetree
reload(unfolder.facetree)

# second level
import unfolder.analyze_patch
reload(unfolder.analyze_patch)

import unfolder.analyze_patch.papersize
reload(unfolder.analyze_patch.papersize)

import unfolder.automatic_unfold
reload(unfolder.automatic_unfold)

import unfolder.automatic_unfold.generate_facetree
import unfolder.automatic_unfold.selected_faces
reload(unfolder.automatic_unfold.generate_facetree)
reload(unfolder.automatic_unfold.selected_faces)

import unfolder.create_patch
reload(unfolder.create_patch)

import unfolder.create_patch.patch
import unfolder.create_patch.patch_builder
reload(unfolder.create_patch.patch)
reload(unfolder.create_patch.patch_builder)

import unfolder.select_facetree
reload(unfolder.select_facetree)

import unfolder.select_facetree.select_facetree_states
import unfolder.select_facetree.select_facetree_context
reload(unfolder.select_facetree.select_facetree_states)
reload(unfolder.select_facetree.select_facetree_context)

import unfolder.util
reload(unfolder.util)

import unfolder.util.helpers
import unfolder.util.plane_coordinate_system
import unfolder.util.selection
reload(unfolder.util.helpers)
reload(unfolder.util.plane_coordinate_system)
reload(unfolder.util.selection)
