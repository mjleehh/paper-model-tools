class ObjectFileReader:

    def __init__(self):
        self.vertices = []
        self.normals = []
        self.edges = []
        self.faces = []
        self.initHandlers()

    def initHandlers(self):

    def read(self,  file):
        with open(file) as f:
            for line in f:
                self.handleLine(line)


    def handleLine(self, line):
        words = line.split()
        if words:
            verb = words[0]
            Hanlder()