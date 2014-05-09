class PatchBase:
    def __init__(self, connection, parentFace, inBaseEdge, baseEdge):
        self.connection = connection
        self.parentFace = parentFace
        self.inBaseEdge = inBaseEdge
        self.baseEdge = baseEdge
