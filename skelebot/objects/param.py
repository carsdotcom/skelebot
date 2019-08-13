"""Param Class"""

from schema import Schema, And, Optional
from .skeleYaml import SkeleYaml

class Param(SkeleYaml):
    """
    Param Class

    The Param Class defines a single parameter that can be passed to a job in a Skelebot project
    """

    schema = Schema({
        'name': And(str, error='Param \'name\' must be a String'),
        Optional('alt'): And(str, error='Param \'alt\' must be a String'),
        Optional('accepts'): And(str, error='Param \'accepts\' must be a String'),
        Optional('choices'): And(list, error='Param \'choices\' must be a List'),
        Optional('help'): And(str, error='Param \'help\' must be a String')
    }, ignore_extra_keys=True)

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
