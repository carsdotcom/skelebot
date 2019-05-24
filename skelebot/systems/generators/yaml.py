from ...objects.config import Config
from ...objects.job import Job
from ...objects.component import Activation
from ...components.componentFactory import ComponentFactory
from ...components.plugin import Plugin

import yaml
import os

COMPONENTS_ATTRIBUTE = "components"
FILE_PATH = "{path}/skelebot.yaml"
ENV_FILE_PATH = "{path}/skelebot-{env}.yaml"

# Attempts to load the skelebot.yaml file into a Config object along with all of the activated componenets
def loadConfig(env=None):

    yamlData = readYaml(env)

    config = None
    if (yamlData is None):
        config = Config()
    else:
        values = {}
        for attr in yamlData.keys():
            if (attr in list(vars(Config).keys())) and (attr != COMPONENTS_ATTRIBUTE):
                if (attr == "jobs"):
                    values[attr] = Job.loadList(yamlData[attr])
                elif (yamlData[attr] == '{VERSION}'):
                    with open('VERSION', 'r') as version:
                        values[attr] = version.read().replace("\n", "")
                else:
                    values[attr] = yamlData[attr] if (attr in yamlData) else None

        config = Config(**values)

    config.components = loadComponents(yamlData)

    return config

# Given a Config object, this function will generate the skelebot.yaml file with the values in the object
def saveConfig(config):
    yml = yaml.dump(config.toDict(), default_flow_style=False)
    skelebotYaml = open(FILE_PATH.format(path=os.getcwd()), "w")
    skelebotYaml.write(yml)
    skelebotYaml.close()

# Reads the skelebot.yaml file (and env override if present) from the current path and loads it into a dict if present
def readYaml(env=None):
    yamlData = None
    cfgFile = FILE_PATH.format(path=os.getcwd())
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            yamlData = yaml.load(stream)
            if (env is not None):
                envFile = ENV_FILE_PATH.format(path=cwd, env=env)
                if os.path.isfile(envFile):
                    with open(envFile, 'r') as stream:
                        override = yaml.load(stream)
                        yamlData = override(yamlData, override)

    return yamlData

# Override one dictionary with data from another dictionary
def override(orig, over):
    merged = copy.deepcopy(orig)
    for k, v2 in over.items():
        if k in merged:
            v1 = merged[k]
            if isinstance(v1, dict) and isinstance(v2, collections.Mapping):
                merged[k] = {**v1, **v2}
            else:
                merged[k] = copy.deepcopy(v2)
        else:
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
