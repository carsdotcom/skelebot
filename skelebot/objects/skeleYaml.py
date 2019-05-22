import copy

class SkeleYaml():

    def toDict(self):
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
