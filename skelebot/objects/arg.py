"""Job Argument Class"""

from .skeleYaml import SkeleYaml

class Arg(SkeleYaml):
    """
    Argument Class

    Defines a single, required, positional argument for a job in the skelebot config
    """

    name = None
    choices = None
    help = None

    def __init__(self, name, choices=None, help=None):
        """Initialize the attributes of the argument"""

        self.name = name
        self.choices = choices
        self.help = help

    @classmethod
    def load(cls, config):
        """Load the class object from the provided config"""

        return cls(**config)

    @classmethod
    def loadList(cls, configs):
        """Load a list of Arg objects from a config list"""

        args = []
        for config in configs:
            args.append(cls.load(config))

        return args
