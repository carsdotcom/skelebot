from ..globals import COMPONENTS
from ..globals import DESCRIPTION
from ..globals import VERSION
import argparse
import sys

# Construct the Argument Parser based on the config file and parse the args that were passed in
def parseArgs(config=None):
    env = getEnvironment()
    desc = getDescription(config)

    # Construct the root argument parser from which all sub-parsers will be built
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="job")

    # Add all the component subparsers to the root parser
    for component in COMPONENTS:
        subparsers = component.addParsers(subparsers)

    args = parser.parse_args()
    return args

# Obtain the environment parameter from the skelebot command string
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
def getDescription(config=None):
    description = "Skelebot Version: {version}".format(version=VERSION)
    if (config != None):
        name = " ".join([word.capitalize() for word in config.name.split("-")])
        description = config.description
        version = config.version
        sbVersion = config.skelebotVersion
        description = DESCRIPTION.format(sbVersion=sbVersion, version=VERSION, project=name, desc=desc, pVersion=version, env=env)

    return description
