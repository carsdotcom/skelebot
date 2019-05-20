from .skeleYaml import SkeleYaml
from enum import Enum

class Activation(Enum):
    EMPTY = 1
    CONFIG = 2
    PROJECT = 3
    ALWAYS = 4

class Component(SkeleYaml):
    activation = Activation.CONFIG
    commands = []

    @classmethod
    def load(cls, config): return cls(**config)

    # Scaffolding System Hooks
    def scaffold(self): return None

    # Parsing System Hooks
    def addParsers(self, subparsers): return subparsers

    # Generator System Hooks
    def appendDockerignore(self): return ""
    def appendDockerfile(self): return ""

    # Execution System Hooks
    def execute(self, config, args): return None
    def prependCommand(self, job, native): return None
    def appendCommand(self, job, native): return None
    def addDockerRunParams(self): return None
