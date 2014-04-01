print('reloading')

# top level
import unfolder
reload(unfolder)

# first level
import unfolder.tree.Tree
import unfolder.graph
reload(unfolder.tree.Tree)
reload(unfolder.graph)

# second level
import unfolder.analyze_patch
reload(unfolder.analyze_patch)

import unfolder.analyze_patch.papersize
import unfolder.analyze_patch.inner_vertex_checker
import unfolder.analyze_patch.line_intersection_checker
reload(unfolder.analyze_patch.papersize)
reload(unfolder.analyze_patch.inner_vertex_checker)
reload(unfolder.analyze_patch.line_intersection_checker)

import unfolder.automatic_unfold
reload(unfolder.automatic_unfold)

import unfolder.automatic_unfold.create_paper_model_command
import unfolder.automatic_unfold.create_paper_model_command2
import unfolder.automatic_unfold.generate_facetree
import unfolder.automatic_unfold.selected_faces
import unfolder.automatic_unfold.test_collision
import unfolder.automatic_unfold.mesh_to_graph
reload(unfolder.automatic_unfold.create_paper_model_command)
reload(unfolder.automatic_unfold.create_paper_model_command2)
reload(unfolder.automatic_unfold.generate_facetree)
reload(unfolder.automatic_unfold.selected_faces)
reload(unfolder.automatic_unfold.test_collision)
reload(unfolder.automatic_unfold.mesh_to_graph)

import unfolder.patch
reload(unfolder.patch)

import unfolder.patch.patch
import unfolder.patch.patch_builder
import unfolder.patch.face_utils
reload(unfolder.patch.patch)
reload(unfolder.patch.patch_builder)
reload(unfolder.patch.face_utils)

import unfolder.mesh
reload(unfolder.mesh)

import unfolder.mesh.maya_mesh
import unfolder.mesh.obj_importer
import unfolder.mesh.obj_mesh
reload(unfolder.mesh.maya_mesh)
reload(unfolder.mesh.obj_importer)
reload(unfolder.mesh.obj_mesh)

import unfolder.select_facetree
reload(unfolder.select_facetree)

import unfolder.select_facetree.create_paper_model_tool
import unfolder.select_facetree.select_facetree_context
import unfolder.select_facetree.state_factory
reload(unfolder.select_facetree.create_paper_model_tool)
reload(unfolder.select_facetree.select_facetree_context)
reload(unfolder.select_facetree.state_factory)

import unfolder.select_facetree.states
reload(unfolder.select_facetree.states)

import unfolder.select_facetree.states.util
import unfolder.select_facetree.states.state
import unfolder.select_facetree.states.add_faces_to_strip
import unfolder.select_facetree.states.do_nothing
import unfolder.select_facetree.states.select_initial_face
import unfolder.select_facetree.states.select_object
import unfolder.select_facetree.states.select_strip_root
reload(unfolder.select_facetree.states.util)
reload(unfolder.select_facetree.states.state)
reload(unfolder.select_facetree.states.add_faces_to_strip)
reload(unfolder.select_facetree.states.do_nothing)
reload(unfolder.select_facetree.states.select_initial_face)
reload(unfolder.select_facetree.states.select_object)
reload(unfolder.select_facetree.states.select_strip_root)

import unfolder.util
reload(unfolder.util)

import unfolder.util.functional
import unfolder.util.helpers
import unfolder.util.plane_coordinate_system
import unfolder.util.selection
reload(unfolder.util.functional)
reload(unfolder.util.helpers)
reload(unfolder.util.plane_coordinate_system)
reload(unfolder.util.selection)
