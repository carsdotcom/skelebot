from .skeleYaml import SkeleYaml

class Param(SkeleYaml):
    name = None
    alt = None
    default = None
    choices = None
    isBoolean = None
    help = None

    def __init__(self, name=None, alt=None, default=None, choices=[], isBoolean=False, help=None):
        self.name = name
        self.alt = alt
        self.default = default
        self.choices = choices
        self.isBoolean = isBoolean
        self.help = help

    @classmethod
    def load(cls, config):
        return cls(**config)

    @classmethod
    def loadList(cls, config):
        params = []
        for element in config:
            params.append(cls.load(element))

        return params
