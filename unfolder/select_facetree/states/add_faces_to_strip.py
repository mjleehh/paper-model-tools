from .do_nothing import DoNothing


class AddFacesToStrip(DoNothing):

    def __init__(self, context, dagPath, initialNode, facetree):
        print('add faces to strip init')
        DoNothing.__init__(self, context)
        self._initialNode = initialNode