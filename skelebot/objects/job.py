"""Job Class"""

from .skeleYaml import SkeleYaml
from .param import Param
from .arg import Arg

class Job(SkeleYaml):
    """
    Job Class

    Config class that defines a job in a Skelebot project via the config yaml file
    """

    name = None
    source = None
    mode = None
    help = None
    args = None
    params = None
    ignores = None
    mappings = None

    def __init__(self, name=None, source=None, mode=None, help=None, args=None, params=None,
                 ignores=None, mappings=None):
        """Initialize the job object with all provided optional attributes"""

        self.name = name
        self.source = source
        self.help = help
        self.mode = mode if mode is not None else "i"
        self.args = args if args is not None else []
        self.params = params if params is not None else []
        self.ignores = ignores if ignores is not None else []
        self.mappings = mappings if mappings is not None else []

    @classmethod
    def load(cls, config):
        """
        Defines the customer manner in which the object is loaded from a Dict due to the nature of
        args and params needing to be loaded differently since they are lists of objects that need
        to be instantiated
        """

        values = {}
        for attr in config.keys():
            if attr in list(vars(Job).keys()):
                if attr == "args":
                    values[attr] = Arg.loadList(config[attr])
                elif attr == "params":
                    values[attr] = Param.loadList(config[attr])
                else:
                    values[attr] = config[attr]

        return cls(**values)

    @classmethod
    def loadList(cls, config):
        """Iterates over a list of Dicts that represent job objects and loads them into a list"""

        jobs = []
        for element in config:
            jobs.append(cls.load(element))

        return jobs
