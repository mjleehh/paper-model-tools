import unfolder.select_facetree.states.select_object


def createInitialState(context):
    return unfolder.select_facetree.states.select_object.SelectObject(context).ffwd()
