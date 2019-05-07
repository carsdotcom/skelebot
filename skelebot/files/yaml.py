from ..objects.config import Config
from ..components.activeComponents import getComponent

import yaml
import os

# Attempts to load the skelebot.yaml file into a Config object along with all of the associated
# componenets in a list
def loadConfig():

    config = None

    # Read the skelebot config file if it is present
    cwd = os.getcwd()
    cfgFile = "{path}/skelebot.yaml".format(path=cwd)
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            cfg = yaml.load(stream)
            values = {}
            for attr in Config.getOrderedAttrs():
                if (attr in cfg):
                    if (attr == "components"):
                        # Load the component object by name using it's Class from the global mapping
                        values[attr] = []
                        for compName in cfg[attr]:
                            compClass = getComponent(compName)
                            if (compClass != None):
                                component = compClass.load(cfg[attr][compName])
                                values[attr].append(component)
                    else:
                        values[attr] = cfg[attr]
                else:
                    # Attribute is not present in skelebot.yaml, set it to None
                    values[attr] = None
            config = Config(**values)

    return config

# Given a Config object, this function will generate the skelebot.yaml file with the values in the object
#def saveConfig(config):
