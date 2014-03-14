from .state import State


class DoNothing:
    """ Final state of the face tree selection tool.

        Do nothing on input. When the context has been completed it remains in
        this state.
    """

    # event callbacks

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
