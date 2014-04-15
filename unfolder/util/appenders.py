class Appender:
    def __init__(self):
        self.store = []

    def push(self, elem):
        index = len(self.store)
        self.store.append(elem)
        return index

class IfNewAppender:
    def __init__(self):
        self.store = []
        self.mapping = {}

    def push(self, elem):
        if elem in self.mapping:
            return self.mapping[elem]
        else:
            index = len(self.store)
            self.store.append(elem)
            self.mapping[elem] = index
            return index
