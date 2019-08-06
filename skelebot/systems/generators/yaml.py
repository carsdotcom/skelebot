"""YAML Generator"""

import os
import copy
import yaml
from ...objects.config import Config
from ...objects.job import Job
from ...objects.param import Param
from ...objects.component import Activation
from ...components.componentFactory import ComponentFactory

COMPS_ATTR = "components"
VERSION_ATTR = "version"
FILE_PATH = "{path}/skelebot.yaml"
VERSION_PATH = "{path}/VERSION"
ENV_FILE_PATH = "{path}/skelebot-{env}.yaml"

def loadVersion():
    """Load the version number from the VERSION file"""

    version = "0.0.0"
    with open(VERSION_PATH.format(path=os.getcwd()), 'r') as file:
        version = file.read().replace("\n", "")
    return version

def saveVersion(version):
    """Overwrite the version number in the VERSION file with a new version"""

    with open(VERSION_PATH.format(path=os.getcwd()), 'w') as file:
        file.write(version)

def loadConfig(env=None):
    """
    Attempt to load the skelebot.yaml file into a Config object along with all of the activated
    componenets
    """

    yamlData = readYaml(env)

    config = None
    if (yamlData is None):
        config = Config()
    else:
        values = {}
        values[VERSION_ATTR] = loadVersion()
        for attr, value in yamlData.items():
            if (attr in vars(Config)) and (attr != COMPS_ATTR) and (attr != VERSION_ATTR):

                if (attr == "jobs"):
                    values[attr] = Job.loadList(value)
                elif (attr == "params"):
                    values[attr] = Param.loadList(value)
                else:
                    values[attr] = value

        config = Config(**values)

    config.components = loadComponents(yamlData)

    return config

def saveConfig(config):
    """Generate the skelebot.yaml and VERSION files with the values from the Config object"""

    saveVersion(config.version)
    config.version = None
    yml = yaml.dump(config.toDict(), default_flow_style=False)

    with open(FILE_PATH.format(path=os.getcwd()), "w") as file:
        file.write(yml)

def readYaml(env=None):
    """Load the skelebot.yaml, with environment overrride if present, into the Config object"""

    yamlData = None
    cwd = os.getcwd()
    cfgFile = FILE_PATH.format(path=cwd)
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            yamlData = yaml.load(stream, Loader=yaml.FullLoader)
            if (env is not None):
                envFile = ENV_FILE_PATH.format(path=cwd, env=env)
                if os.path.isfile(envFile):
                    with open(envFile, 'r') as stream:
                        overrideYaml = yaml.load(stream, Loader=yaml.FullLoader)
                        yamlData = override(yamlData, overrideYaml)

    return yamlData

def override(orig, over):
    """Override one dictionary with data from another dictionary"""

    merged = copy.deepcopy(orig)
    for k, v2 in over.items():
        merged[k] = copy.deepcopy(v2)
    return merged

def loadComponents(yamlData):
    """
    Parses the components section of skelebot.yaml config to generate the complete list of
    components for the project based on the active component list and each components' Activation
    attribute
    """

    components = []
    componentFactory = ComponentFactory()
    if (yamlData is None):
        components = componentFactory.buildComponents([Activation.EMPTY, Activation.ALWAYS])
    else:
        compNames = []
        if (COMPS_ATTR in yamlData):
            yamlConfig = yamlData[COMPS_ATTR]
            for compName in yamlConfig:
                component = componentFactory.buildComponent(compName, yamlConfig[compName])
                if (component is not None):
                    components.append(component)
                    compNames.append(component.__class__.__name__)

        activations = [Activation.PROJECT, Activation.ALWAYS]
        components.extend(componentFactory.buildComponents(activations, ignores=compNames))

    return components
