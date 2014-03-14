class State(object):
    def __init__(self, stateFactory, previous):
        self._stateFactory = stateFactory
        self._previous = previous

    # methods

    def ffwd(self):
        nextState = self._nextState()
        if nextState:
            return nextState()
        else:
            return self.reset()

    def reset(self):
#        self._context.setHelpString(self._helpString())
        self._waitForInput()
        return self

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
        return self._previous()

    def complete(self):
        print('nothing complete')
        return self

    def abort(self):
        print('nothing abort')
        return self