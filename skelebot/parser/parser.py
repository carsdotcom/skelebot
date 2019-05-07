from ..components.activeComponents import getComponents
from ..common import DESCRIPTION
from ..common import VERSION
import argparse
import sys

# Construct the Argument Parser based on the config file and parse the args that were passed in
def parseArgs(config=None):

    env = getEnvironment()
    desc = getDescription(env, config)

    # Construct the root argument parser from which all sub-parsers will be built
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="job")

    # Identify and load component parsers from the master list based on their activation value
    for componentClass in getComponents():
        component = config.getComponent(componentClass.__name__) if (config != None) else None
        activation = componentClass.activation

        # TODO: Need to move this logic into the YAML loading process so the config object can simply be used as intended
        # TODO: Should be able to clean up this logic, but make sure it's working first #TruthTableForTheWin
        if (activation == Activation.EMPTY) and (config is None): # Activate if the command was run outside of a skelebot project
            subparsers = componentClass().addParsers(subParsers)
        elif (activation == Activation.CONFIG) and (component != None): # Activate if the component is present in the config
            subparsers = component.addParsers(subParsers)
        elif (activation == Activation.PROJECT) and (config != None): # Add as long as there is a project present
            component = componentClass() if (component is None) else component
            subparsers = component.addParsers(subParsers)
        elif (activation == Activation.ALWAYS): # Add no matter what
            component = componentClass() if (component is None) else component
            subparsers = component.addParsers(subParsers)

    args = parser.parse_args()
    return args

# Obtain the environment parameter from the skelebot command string prior to contructing the arg parser
def getEnvironment():
    isNext = False
    env = None
    for arg in sys.argv:
        if (isNext):
            env = arg
            break

        if (arg == "-e") or (arg == "--env"):
            isNext = True

    return env

# Construct the description text for the '--help' output
def getDescription(env, config=None):
    description = "Skelebot Version: {version}".format(version=VERSION)
    if (config != None):
        name = " ".join([word.capitalize() for word in config.name.split("-")])
        description = config.description
        version = config.version
        sbVersion = config.skelebotVersion
        description = DESCRIPTION.format(sbVersion=sbVersion, version=VERSION, project=name, desc=description, pVersion=version, env=env)

    return description
