"""SkeleYaml Base Object"""

import copy

class SkeleYaml():
    """
    SkeleYaml Class

    This class acts as a base for any object that needs to be converted to a Dict for YAML file
    generation purposes
    """

    def toDict(self):
        """Convert the object attributes into a Dict structure that is ready for YAML generation"""

        dct = copy.deepcopy(vars(self))
        removeList = []
        for key in dct.keys():
            if (dct[key] is None) or (dct[key] == []):
                removeList.append(key)
            elif (isinstance(dct[key], SkeleYaml)):
                dct[key] = dct[key].toDict()
            elif (isinstance(dct[key], list)):
                dctList = []
                for element in dct[key]:
                    dctList.append(element.toDict() if isinstance(element, SkeleYaml) else element)
                dct[key] = dctList

        for key in removeList:
            del dct[key]

        return dct
