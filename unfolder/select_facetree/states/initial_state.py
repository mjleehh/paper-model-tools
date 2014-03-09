from .select_object import SelectObject


def createInitialState(context):
    return SelectObject(context).ffwd()
