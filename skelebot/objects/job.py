from .skeleYaml import SkeleYaml
from .param import Param
from .arg import Arg

class Job(SkeleYaml):
    name = None
    source = None
    mode = None
    help = None
    args = None
    params = None
    ignores = None
    mappings = None

    def __init__(self, name=None, source=None, mode=None, help=None, args=[], params=[], ignores=[], mappings=[]):
        self.name = name
        self.source = source
        self.mode = "i" if mode == None else mode
        self.help = help
        self.args = args
        self.params = params
        self.ignores = ignores
        self.mappings = mappings

    @classmethod
    def load(cls, config):
        values = {}
        for attr in config.keys():
            if (attr in list(vars(Job).keys())):
                if (attr == "args"):
                    values[attr] = Arg.loadList(config[attr])
                elif (attr == "params"):
                    values[attr] = Param.loadList(config[attr])
                else:
                    values[attr] = config[attr]

        return cls(**values)

    @classmethod
    def loadList(cls, config):
        jobs = []
        for element in config:
            jobs.append(cls.load(element))

        return jobs
