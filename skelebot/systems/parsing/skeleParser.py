from ...common import DESCRIPTION
from ...common import VERSION
import argparse
import sys

# SkeleParser is a wrapper around the parsing object that allows it to possbily be replaced in the future with custom logic
class SkeleParser:

    parser = None
    config = None
    env = None
    desc = None
    
    def __init__(self, config=None, env=None):
        self.config = config
        self.env = env
        self.desc = self.buildDescription()

        # Construct the root argument parser from which all sub-parsers will be built
        self.parser = argparse.ArgumentParser(description=self.desc, formatter_class=argparse.RawTextHelpFormatter)
        subparsers = self.parser.add_subparsers(dest="job")

        # Add the parsers from the active components in the config
        for component in self.config.components:
            subparsers = component.addParsers(subparsers)

    # Construct the Argument Parser based on the config file and parse the args that were passed in
    def parseArgs(self):
        return self.parser.parse_args()

    # Display the help message from the internal parser object
    def showHelp(self):
        return self.parser.print_help()

    # Construct the description text for the '--help' output
    def buildDescription(self):
        description = "Skelebot Version: {version}".format(version=VERSION)
        if (self.config.name != None):
            name = " ".join([word.capitalize() for word in self.config.name.split("-")])
            description = self.config.description
            version = self.config.version
            sbVersion = self.config.skelebotVersion
            description = DESCRIPTION.format(sbVersion=sbVersion, version=VERSION, project=name, desc=description, pVersion=version, env=self.env)

        return description
