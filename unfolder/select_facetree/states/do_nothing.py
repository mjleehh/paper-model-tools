class DoNothing():
    """ Final state of the face tree selection tool.

        Do nothing on input. When the context has been completed it remains in
        this state.
    """
    def __init__(self, context):
        self._context = context

    def init(self):
        self._context.setHelpString('face tree selection tool done')
        return self

    def advance(self, nextState):
        print('advance')
        return nextState.init()

    def doPress(self, event):
        print('nothing do press')
        return self

    def doDrag(self, event):
        print('nothing do drag')
        return self

    def doRelease(self, event):
        print('nothing do release')
        return self

    def delete(self):
        print('nothing delete')
        return self

    def complete(self):
        print('nothing complete')
        return self

    def abort(self):
        print('nothing abort')
        return self
