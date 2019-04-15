from .yaml import *

class Jupyter(YamlClass):
    port = None
    folder = None

    def __init__(self, port=8888, folder="."):
        self.port = port
        self.folder = folder

    @classmethod
    def getOrderedAttrs(cls):
        return ["port", "folder"]
