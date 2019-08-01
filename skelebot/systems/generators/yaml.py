from ...objects.config import Config
from ...objects.job import Job
from ...objects.param import Param
from ...objects.component import Activation
from ...components.componentFactory import ComponentFactory
from ...components.plugin import Plugin

import yaml
import os
import copy

COMPONENTS_ATTRIBUTE = "components"
VERSION_ATTRIBUTE = "version"
FILE_PATH = "{path}/skelebot.yaml"
VERSION_PATH = "{path}/VERSION"
ENV_FILE_PATH = "{path}/skelebot-{env}.yaml"

def loadVersion():
    version = "0.0.0"
    with open(VERSION_PATH.format(path=os.getcwd()), 'r') as file:
        version = file.read().replace("\n", "")
    return version

def saveVersion(version):
    with open(VERSION_PATH.format(path=os.getcwd()), 'w') as file:
        file.write(version)

# Attempts to load the skelebot.yaml file into a Config object along with all of the activated componenets
def loadConfig(env=None):

    yamlData = readYaml(env)

    config = None
    if (yamlData is None):
        config = Config()
    else:
        values = {}
        values[VERSION_ATTRIBUTE] = loadVersion()
        for attr, value in yamlData.items():
            if (attr in vars(Config)) and (attr != COMPONENTS_ATTRIBUTE) and (attr != VERSION_ATTRIBUTE):
                if (attr == "jobs"):
                    values[attr] = Job.loadList(value)
                elif (attr == "params"):
                    values[attr] = Param.loadList(value)
                else:
                    values[attr] = value

        config = Config(**values)

    config.components = loadComponents(yamlData)

    return config

# Given a Config object, this function will generate the skelebot.yaml file with the values in the object
def saveConfig(config):
    saveVersion(config.version)
    config.version = None
    yml = yaml.dump(config.toDict(), default_flow_style=False)

    with open(FILE_PATH.format(path=os.getcwd()), "w") as file:
        file.write(yml)

# Reads the skelebot.yaml file (and env override if present) from the current path and loads it into a dict if present
def readYaml(env=None):
    yamlData = None
    cwd = os.getcwd()
    cfgFile = FILE_PATH.format(path=cwd)
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            yamlData = yaml.load(stream)
            if (env is not None):
                envFile = ENV_FILE_PATH.format(path=cwd, env=env)
                if os.path.isfile(envFile):
                    with open(envFile, 'r') as stream:
                        overrideYaml = yaml.load(stream)
                        yamlData = override(yamlData, overrideYaml)

    return yamlData

# Override one dictionary with data from another dictionary
def override(orig, over):
    merged = copy.deepcopy(orig)
    for k, v2 in over.items():
        merged[k] = copy.deepcopy(v2)
    return merged

# Parses the components section of skelebot.yaml config to generate the complete list of components
# for the project based on the active component list and each components Activation attribute
def loadComponents(yamlData):

    components = []
    componentFactory = ComponentFactory()
    if (yamlData is None):
        components = componentFactory.buildComponents([Activation.EMPTY, Activation.ALWAYS])
    else:
        compNames = []
        if (COMPONENTS_ATTRIBUTE in yamlData):
            yamlConfig = yamlData[COMPONENTS_ATTRIBUTE]
            for compName in yamlConfig:
                component = componentFactory.buildComponent(compName, yamlConfig[compName])
                if (component is not None):
                    components.append(component)
                    compNames.append(component.__class__.__name__)

        components.extend(componentFactory.buildComponents([Activation.PROJECT, Activation.ALWAYS], ignores=compNames))

    return components
