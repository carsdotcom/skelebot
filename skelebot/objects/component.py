from enum import Enum

class Activation(Enum):
    EMPTY = 1
    CONFIG = 2
    PROJECT = 3
    ALWAYS = 4

class Component():
    activation = Activation.CONFIG

    @classmethod
    def load(cls, config): return None

    def addParsers(self, subparsers): return subparsers
