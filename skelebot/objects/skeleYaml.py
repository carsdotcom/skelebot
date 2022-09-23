"""SkeleYaml Base Object"""

import copy

class SkeleYaml():
    """
    SkeleYaml Class

    This class acts as a base for any object that needs to be converted to a Dict for YAML file
    generation purposes
    """

    schema = None

    @classmethod
    def loadList(cls, config):
        """Iterates over a list of Dicts that represent SkeleYamls and loads them into a list"""

        objs = []
        if isinstance(config, list):
            for element in config:
                objs.append(cls.load(element))

        return objs

    @classmethod
    def load(cls, config):
        """Defines the default manner of loading a Component object from a config dict"""

        cls.validate(config)
        return cls(**config)

    @classmethod
    def validate(cls, config):
        """Executes the schema validation based on the defined Schema for the implemented class"""

        if cls.schema is not None:
            cls.schema.validate(config)

    def toDict(self):
        """Convert the object attributes into a Dict structure that is ready for YAML generation"""

        dct = copy.deepcopy(vars(self))
        removeList = []
        for key, value in dct.items():
            if (value is None) or (value == []):
                removeList.append(key)
            elif (isinstance(value, SkeleYaml)):
                dct[key] = value.toDict()
            elif (isinstance(value, list)):
                dctList = []
                for element in value:
                    dctList.append(element.toDict() if isinstance(element, SkeleYaml) else element)
                dct[key] = dctList
            elif (isinstance(value, dict)):
                dctDict = {}
                for item_key, item_value in value.items():
                    dctDict[item_key] = item_value.toDict() if (isinstance(item_value, SkeleYaml)) else item_value
                dct[key] = dctDict

        for key in removeList:
            del dct[key]

        return dct
