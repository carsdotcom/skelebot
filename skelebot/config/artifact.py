from .yaml import *
from .deploy import *

class Artifact(YamlClass):
    'Config object for the project artifact details'
    name = None
    file = None
    deploy = None

    def __init__(self, name, file, deploy):
        self.name = name
        self.file = file
        self.deploy = deploy

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "file", "deploy"]

    @classmethod
    def load(cls, cfg):
        values = {}
        for attr in cls.getOrderedAttrs():
            if (attr in cfg):
                if (attr == "deploy"):
                    values[attr] = Deploy.load(cfg[attr])
                else:
                    values[attr] = cfg[attr]
            else:
                values[attr] = None
        return cls(**values)
