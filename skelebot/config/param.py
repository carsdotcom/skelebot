from .yaml import *

class Param(YamlClass):
    'Config object for skelebot job params and arguments'
    name = None
    alt = None
    default = None
    choices = None

    def __init__(self, name, alt, default=None, choices=None):
        self.name = name
        self.alt = alt
        self.default = default
        self.choices = choices

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "alt", "default", "choices"]
