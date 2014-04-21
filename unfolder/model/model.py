from unfolder.model.model_impl import ModelImpl
from unfolder.model.patch import PatchIter


class Model:
    def __init__(self, impl: ModelImpl):
        self.impl = impl

    @property
    def patches(self):
        return PatchIter(self.impl)
