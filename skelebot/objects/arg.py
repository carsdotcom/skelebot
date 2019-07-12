from .skeleYaml import SkeleYaml

class Arg(SkeleYaml):
    name = None
    choices = None
    help = None

    def __init__(self, name, choices=None, help=None):
        self.name = name
        self.choices = choices
        self.help = help

    @classmethod
    def load(cls, config):
        return cls(**config)

    @classmethod
    def loadList(cls, config):
        args = []
        for element in config:
            args.append(cls.load(element))

        return args
