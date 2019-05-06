from ..globals import ACTIVATION.CONFIG

class Component():

    @classmethod
    def load(cls, config): return None

    @classmethod
    def getOrderedAttrs(cls): return []

    @classmethod
    def activationLevel(cls): return ACTIVATION.CONFIG

    def addParsers(self, subparsers): return subparsers
