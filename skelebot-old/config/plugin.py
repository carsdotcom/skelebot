from .yaml import *

class Plugin(YamlClass):
    name = None
    config = None

    def __init__(self, name, config):
        self.name = name
        self.config = config

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "config"]
