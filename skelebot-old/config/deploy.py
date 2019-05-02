from .yaml import *

class Deploy(YamlClass):
    'Config object for the project artifact deployment details'
    type = None
    url = None
    repo = None
    path = None

    def __init__(self, type, url, repo, path):
        self.type = type
        self.url = url
        self.repo = repo
        self.path = path

    @classmethod
    def getOrderedAttrs(cls):
        return ["type", "url", "repo", "path"]
