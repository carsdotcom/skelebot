from ..objects.config import Config
from ..components.activeComponents import getComponent

import yaml
import os

COMPONENTS_ATTRIBUTE = "components"

# Attempts to load the skelebot.yaml file into a Config object along with all of the activated componenets 
def loadConfig():

    config = readYaml()
    if (config != None):
        values = {}
        for attr in Config.getOrderedAttrs():
            value = None
            if (attr in cfg):
                if (attr == COMPONENTS_ATTRIBUTE):
                    value = loadComponents(cfg[COMPONENTS_ATTRIBUTE])
                else:
                    value = cfg[attr]
            values[attr] = value

        config = Config(**values)

    return config

# Reads the skelebot.yaml file from the current path and loads it into a dict if present
def readYaml():
    config = None
    cwd = os.getcwd()
    cfgFile = "{path}/skelebot.yaml".format(path=cwd)
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            cfg = yaml.load(stream)

    return config


# Parses the components section of skelebot.yaml config to generate the complete list of components
# for the project based on the active component list and each components Activation attribute
def loadComponents(config):

    if (config is None):
        # Since there is no config, loads BASE and ALWAYS activation components with default values
        # TODO
    else:
        # Since there is a config, loads component objects that are present in config and also in the active list
        components = []
        for compName in componentConfig:
            compClass = getComponent(compName)
            if (compClass != None):
                component = compClass.load(cfg[attr][compName])
                components.append(component)

        # Loads additional components that are not in config but are active and available without config (ACTIVATION = ALWAYS | PROJECT)

    return components

# Given a Config object, this function will generate the skelebot.yaml file with the values in the object
#def saveConfig(config):
