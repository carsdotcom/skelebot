"""YAML Generator"""

import os
import copy
import yaml
from ...objects.config import Config

FILE_PATH = "{path}/skelebot.yaml"
VERSION_PATH = "{path}/VERSION"
ENV_FILE_PATH = "{path}/skelebot-{env}.yaml"

def loadConfig(env=None):
    """
    Attempt to load the skelebot.yaml file into a Config object along with all of the activated
    componenets
    """

    config = Config.load(readYaml(env))
    config.env = env
    config.version = loadVersion()
    return config

def saveConfig(config):
    """Generate the skelebot.yaml and VERSION files with the values from the Config object"""

    saveVersion(config.version)
    config.version = None
    yml = yaml.dump(config.toDict(), default_flow_style=False)

    with open(FILE_PATH.format(path=os.getcwd()), "w") as file:
        file.write(yml)

def loadVersion():
    """Load the version number from the VERSION file"""

    version = None
    versionFile = VERSION_PATH.format(path=os.getcwd())
    if os.path.isfile(versionFile):
        with open(versionFile, 'r') as file:
            version = file.read().replace("\n", "")
    return version

def saveVersion(version):
    """Overwrite the version number in the VERSION file with a new version"""

    with open(VERSION_PATH.format(path=os.getcwd()), 'w') as file:
        file.write(version)

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
                else:
                    raise RuntimeError("Environment Not Found")

    return yamlData

def override(orig, over):
    """Override one dictionary with data from another dictionary"""

    merged = copy.deepcopy(orig)
    for k, v2 in over.items():
        merged[k] = copy.deepcopy(v2)
    return merged
