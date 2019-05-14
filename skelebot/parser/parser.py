from ..common import DESCRIPTION
from ..common import VERSION
import argparse
import sys

# Construct the Argument Parser based on the config file and parse the args that were passed in
def parseArgs(config=None, env=None):

    desc = getDescription(config, env)

    # Construct the root argument parser from which all sub-parsers will be built
    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="job")

    # Add the parsers from the active components in the config
    for component in config.components:
        subparsers = component.addParsers(subparsers)

    args = parser.parse_args()
    return args

# Construct the description text for the '--help' output
def getDescription(config=None, env=None):
    description = "Skelebot Version: {version}".format(version=VERSION)
    if (config.name != None):
        name = " ".join([word.capitalize() for word in config.name.split("-")])
        description = config.description
        version = config.version
        sbVersion = config.skelebotVersion
        description = DESCRIPTION.format(sbVersion=sbVersion, version=VERSION, project=name, desc=description, pVersion=version, env=env)

    return description
