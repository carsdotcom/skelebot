from .yaml import *
from .param import *

class Job(YamlClass):
    'Config object for skelebot jobs'
    name = None
    source = None
    mode = None
    help = None
    args = None
    params = None
    ignore = None
    mapped = None

    def __init__(self, name, source, help, args=None, params=None, ignore=None, mode=None, mapped=None):
        self.name = name
        self.source = source
        self.mode = "i" if mode == None else mode
        self.help = help
        self.args = args
        self.params = params
        self.ignore = ignore
        self.mapped = mapped

    @classmethod
    def getOrderedAttrs(self):
        return ["name", "source", "mode", "help", "mapped", "args", "params", "ignore"]

    @classmethod
    def load(cls, cfg):
        values = {}
        for attr in cls.getOrderedAttrs():
            if (attr in cfg):
                if (attr == "args" or attr == "params"):
                    values[attr] = Param.loadList(cfg[attr])
                else:
                    values[attr] = cfg[attr]
            else:
                values[attr] = None
        return cls(**values)
