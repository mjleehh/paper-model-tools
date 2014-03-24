def hasAtLeastOne(pred, collection):
    for elem in collection:
        if pred(elem):
            return True
    return False


def getFirstOf(pred, collection):
    for elem in collection:
        if pred(elem):
            return elem
    return None


def conditionalTransform(pred, collection):
    return [pred(elem) for elem in collection if pred(elem) is not None]
