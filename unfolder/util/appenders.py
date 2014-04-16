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
        self.indices = {}

    def push(self, elem):
        if elem in self.indices:
            return self.indices[elem]
        else:
            index = len(self.store)
            self.store.append(elem)
            self.indices[elem] = index
            return index

class MappingAppender():
    def __init__(self):
        self.store = []
        self.mapping = {}

    def push(self, key, elem):
        if key in self.mapping:
            return self.mapping[key]
        else:
            index = len(self.store)
            self.store.append(elem)
            self.mapping[key] = index
            return index

    def __getitem__(self, item):
        return self.store[self.mapping[item]]
