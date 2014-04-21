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

    def __getitem__(self, item):
        return self.store[item]


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

    def indexOf(self, item):
        return self.mapping[item]

    def __getitem__(self, item):
        return self.store[self.mapping[item]]


class BucketFiller:
    def __init__(self):
        self.store = []
        self.mapping = {}

    def put(self, key, item):
        index = self.indexOf(key)
        self.store[index] = item
        return index

    def indexOf(self, key):
        if key in self.mapping:
            return self.mapping[key]
        else:
            index = len(self.store)
            self.store.append(None)
            self.mapping[key] = index
            return index


class StackBuckets:
    def __init__(self):
        self.store = {}

    def push(self, key, item):
        if key in self.store:
            self.store[key].append(item)
        else:
            self.store[key] = [item]


