from .skeleYaml import SkeleYaml

class Param(SkeleYaml):
    name = None
    alt = None
    accepts = None
    default = None
    choices = None
    help = None

    def __init__(self, name, alt=None, accepts=None, default=None, choices=None, help=None):
        self.name = name
        self.alt = alt
        self.accepts = accepts
        self.default = default
        self.choices = choices
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
