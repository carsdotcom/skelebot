from ..objects.config import Config
from ..objects.job import Job
from ..objects.component import Activation
from ..components.componentFactory import buildComponent, buildComponents
from ..components.plugin import Plugin

import yaml
import os

COMPONENTS_ATTRIBUTE = "components"
FILE_PATH = "{path}/skelebot.yaml"

# Attempts to load the skelebot.yaml file into a Config object along with all of the activated componenets
def loadConfig():

    yamlData = readYaml()

    config = None
    if (yamlData is None):
        config = Config()
    else:
        values = {}
        for attr in yamlData.keys():
            if (attr in list(vars(Config).keys())) and (attr != COMPONENTS_ATTRIBUTE):
                if (attr == "jobs"):
                    values[attr] = Job.loadList(yamlData[attr])
                else:
                    values[attr] = yamlData[attr] if (attr in yamlData) else None

        config = Config(**values)

    config.components = loadComponents(yamlData)

    return config

# Reads the skelebot.yaml file from the current path and loads it into a dict if present
def readYaml():
    yamlData = None
    cfgFile = FILE_PATH.format(path=os.getcwd())
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            yamlData = yaml.load(stream)

    return yamlData


# Parses the components section of skelebot.yaml config to generate the complete list of components
# for the project based on the active component list and each components Activation attribute
def loadComponents(yamlData):

    components = []
    if (yamlData is None):
        components = buildComponents([Activation.EMPTY, Activation.ALWAYS])
    else:
        compNames = []
        if (COMPONENTS_ATTRIBUTE in yamlData):
            yamlConfig = yamlData[COMPONENTS_ATTRIBUTE]
            for compName in yamlConfig:
                component = buildComponent(compName, yamlConfig[compName])
                if (component is not None):
                    components.append(component)
                    compNames.append(component.__class__.__name__)

        components.extend(buildComponents([Activation.PROJECT, Activation.ALWAYS], ignores=compNames))

    return components

def noop(self, *args, **kw):
    pass

# Given a Config object, this function will generate the skelebot.yaml file with the values in the object
def saveConfig(config):
    #yaml.emitter.Emitter.process_tag = noop
    yml = yaml.dump(config.toDict(), default_flow_style=False)
    skelebotYaml = open(FILE_PATH.format(path=os.getcwd()), "w")
    skelebotYaml.write(yml)
    skelebotYaml.close()
