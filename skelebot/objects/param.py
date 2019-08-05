"""Param Class"""

from .skeleYaml import SkeleYaml

class Param(SkeleYaml):
    """
    Param Class

    The Param Class defines a single parameter that can be passed to a job in a Skelebot project
    """

    name = None
    alt = None
    accepts = None
    default = None
    choices = None
    help = None

    def __init__(self, name, alt=None, accepts=None, default=None, choices=None, help=None):
        """Initialize the param object with all provided optional attributes"""

        self.name = name
        self.alt = alt
        self.accepts = accepts
        self.default = default
        self.choices = choices
        self.help = help

    @classmethod
    def load(cls, config):
        """Loads the Param object from a config Dict"""

        return cls(**config)

    @classmethod
    def loadList(cls, config):
        """Loads a list of Param objects from a list of config Dicts"""

        params = []
        for element in config:
            params.append(cls.load(element))

        return params
