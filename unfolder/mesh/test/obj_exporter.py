from unittest import TestCase
from unfolder.mesh.obj_exporter import ObjExporter
from unfolder.mesh.obj_importer import ObjImporter
from unfolder.mesh.mesh import Mesh
from unfolder.mesh.mesh_impl import EdgeImpl


class ObjImporterTests(TestCase):

    def test_importObj_box(self):
        reader = ObjImporter()
        box = reader.read('resources/box.obj')

        writer = ObjExporter('tmp/junk.obj')
        writer.write(Mesh(box))
