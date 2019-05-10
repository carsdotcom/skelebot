from .skeleYaml import SkeleYaml
from enum import Enum

class Activation(Enum):
    EMPTY = 1
    CONFIG = 2
    PROJECT = 3
    ALWAYS = 4

class Component(SkeleYaml):
    activation = Activation.CONFIG

    @classmethod
    def load(cls, config): return cls(**config)

    def addParsers(self, subparsers): return subparsers
