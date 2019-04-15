import copy
import collections

def constructElement(value, name=None, level=-1, listElem=False):
    element = ""

    if (value != None):

        if (listElem == False):
            element += "  " * level
        if (name != None):
            element += name + ": "

        if (type(value) is str):
            if ("*" in value):
                value = "'{}'".format(value)
            element += value + "\n"
        elif (type(value) is int):
            element += str(value) + "\n"
        elif (type(value) is bool):
            element += str(value) + "\n"
        elif (type(value) is list):
            if (len(value) == 0):
                element = ""
            else:
                element += "\n"
                for lval in value:
                    element += ("  " * level) + "- " + constructElement(lval, level=level, listElem=True)
        elif (type(value) is dict):
            indent = "  " * (level+1)
            for key in value:
                element += "\n" + indent + key + ": " + value[key]
            element += "\n"
        elif (isinstance(value, YamlClass)):
            if (name != None):
                element += "\n"
            for attr in value.getOrderedAttrs():
                val = getattr(value, attr)
                element += constructElement(val, attr, level + 1, listElem=listElem)
                listElem=False

    return element


def override(orig, over):
    merged = copy.deepcopy(orig)
    for k, v2 in over.items():
        if k in merged:
            v1 = merged[k]
            if isinstance(v1, dict) and isinstance(v2, collections.Mapping):
                merged[k] = merge_dicts(v1, v2)
            else:
                merged[k] = copy.deepcopy(v2)
        else:
            merged[k] = copy.deepcopy(v2)
    return merged


class YamlClass:

    @classmethod
    def getOrderedAttrs(cls): raise NotImplementedError
    def getYaml(self): return constructElement(self)

    @classmethod
    def load(cls, cfg):
        values = {}
        for attr in cls.getOrderedAttrs():
            if (attr in cfg):
                values[attr] = cfg[attr]
            else:
                values[attr] = None
        return cls(**values)

    @classmethod
    def loadList(cls, cfg):
        objects = list()
        for obj in cfg:
            objects.append(cls.load(obj))
        return objects
