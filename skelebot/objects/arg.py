"""Job Argument Class"""

from schema import Schema, And, Optional
from .skeleYaml import SkeleYaml

class Arg(SkeleYaml):
    """
    Argument Class

    Defines a single, required, positional argument for a job in the skelebot config
    """

    schema = Schema({
        'name': And(str, error='Arg \'name\' must be a String'),
        Optional('choices'): And(list, error='Arg \'choices\' must be a List'),
        Optional('help'): And(str, error='Arg \'help\' must be a String')
    }, ignore_extra_keys=True)

    name = None
    choices = None
    help = None

    def __init__(self, name, choices=None, help=None):
        """Initialize the attributes of the argument"""

        self.name = name
        self.choices = choices
        self.help = help
