import abc

class Component(abc.ABC):

    @abc.abstractmethod
    def addParsers(self, subparsers):
        return subparsers
