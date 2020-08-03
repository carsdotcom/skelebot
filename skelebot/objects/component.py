"""Component Object"""

from enum import Enum
from .skeleYaml import SkeleYaml

class Activation(Enum):
    """
    Activation Enum

    The activation value defines when a component will be available for use in a Skelebot project

    EMPTY   | Available only when executing Skelebot outside of a project
    CONFIG  | Available only when the component config is inside the skelebot.yaml
    PROJECT | Available when skelebot is run from inside any project, regardless of config
    ALWAYS  | Always available
    """

    EMPTY = 1
    CONFIG = 2
    PROJECT = 3
    ALWAYS = 4

class Component(SkeleYaml):
    """
    Component Class

    This class acts as an abstract class that defines the default, do nothing, behavior for the
    various hooks in the Skelebot Systems
    """

    activation = Activation.CONFIG
    commands = []

    # Scaffolding System Hooks
    def scaffold(self):
        """Defines the default for adding scaffolding functionality to a component"""
        return None

    # Parsing System Hooks
    def addParsers(self, subparsers):
        """Defines the default for adding subparsers to the SkeleParser"""
        return subparsers

    # Generator System Hooks
    def appendDockerignore(self):
        """Defines the default appending contents to the .dockerignore file"""
        return ""
    def appendDockerfile(self):
        """Defines the default appending contents to the Dockerfile"""
        return ""

    # Execution System Hooks
    def execute(self, config, args, host=None):
        """Defines the execution of commands in the component's commands attribute"""
        return None
    def prependCommand(self, job, native):
        """Defines the contents that are prepended to the command from the component"""
        return None
    def appendCommand(self, job, native):
        """Defines the contents that are appended to the command from the component"""
        return None
    def addDockerRunParams(self):
        """Defines the docker run parameters that are added by the component"""
        return None
