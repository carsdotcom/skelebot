from ..objects.component import *

class Jupyter(Component):
    activation = Activation.PROJECT

    port = None
    folder = None

    def __init__(self, port=8888, folder="."):
        self.port = port
        self.folder = folder

    @classmethod
    def load(cls, config):
        return cls(**config)
