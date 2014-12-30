from Products.Five import BrowserView
from .utils import ml_value


class MLValue(BrowserView):

    def __call__(self, name=None, default=None):
        if name is None:
            return self
        return ml_value(self.context, name, default)

    def __getitem__(self, name, default=None):
        return ml_value(self.context, name, default)
