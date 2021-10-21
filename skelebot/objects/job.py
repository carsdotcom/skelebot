"""Job Class"""

from schema import Schema, And, Or, Optional
from .skeleYaml import SkeleYaml
from .param import Param
from .arg import Arg

class Job(SkeleYaml):
    """
    Job Class

    Config class that defines a job in a Skelebot project via the config yaml file
    """

    schema = Schema({
        'name': And(str, error='Job \'name\' must be a String'),
        'source': And(str, error='Job \'source\' must be a String'),
        Optional('mode'): And(str, error='Job \'mode\' must be a String'),
        Optional('native'): And(str, Or('always', 'never', 'optional'),
            error='Job \'native\' must be one of: \'always\', \'never\', \'optional\''),
        Optional('host'): And(str, error='Job \'host\' must be a String'),
        'help': And(str, error='Job \'help\' must be a String'),
        Optional('args'): And(list, error='Job \'args\' must be a List'),
        Optional('params'): And(list, error='Job \'params\' must be a List'),
        Optional('ignores'): And(list, error='Job \'ignores\' must be a List'),
        Optional('mappings'): And(list, error='Job \'mappings\' must be a List'),
        Optional('ports'): And(list, error='\'ports\' must be a List')
    }, ignore_extra_keys=True)

    name = None
    source = None
    mode = None
    native = None
    host = None
    help = None
    args = None
    params = None
    ignores = None
    mappings = None
    ports = None

    def __init__(self, name=None, source=None, mode=None, native=None, host=None, help=None,
                    args=None, params=None, ignores=None, mappings=None, ports=None):
        """Initialize the job object with all provided optional attributes"""

        self.name = name
        self.source = source
        self.help = help
        self.mode = mode if mode is not None else "i"
        self.native = native if native is not None else "optional"
        self.host = host
        self.args = args if args is not None else []
        self.params = params if params is not None else []
        self.ignores = ignores if ignores is not None else []
        self.mappings = mappings if mappings is not None else []
        self.ports = ports if ports is not None else []

    @classmethod
    def load(cls, config):
        """
        Defines the customer manner in which the object is loaded from a Dict due to the nature of
        args and params needing to be loaded differently since they are lists of objects that need
        to be instantiated
        """

        cls.validate(config)

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
