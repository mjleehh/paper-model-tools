import unfolder.select_facetree.states.add_faces_to_strip
import unfolder.select_facetree.states.do_nothing
import unfolder.select_facetree.states.select_initial_face
import unfolder.select_facetree.states.select_object
import unfolder.select_facetree.states.select_strip_root


class StateFactory:

    def initialState(self):
        return unfolder.select_facetree.states.select_object.SelectObject(self).ffwd

    def selectInitialFace(self, previous, dagPath):
        return unfolder.select_facetree.states.select_initial_face.SelectInitialFace(self, previous, dagPath).ffwd

    def addFacesToStrip(self, previous, dagPath, patchBuilder, stripRoot):
        return unfolder.select_facetree.states.add_faces_to_strip.AddFacesToStrip(self, previous, dagPath, patchBuilder, stripRoot).ffwd

    def selectStripRoot(self, previous, dagPath, patchBuilder, facetree):
        return unfolder.select_facetree.states.select_strip_root.SelectStripRoot(self, previous, dagPath, patchBuilder, facetree).ffwd

    def doNothing(self):
        return unfolder.select_facetree.states.do_nothing.DoNothing().ffwd
