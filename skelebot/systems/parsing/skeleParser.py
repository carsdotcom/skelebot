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

        if (config.name is None):
            # Provide Scaffolding Parser for Non-Skelebot Projects
            scaffoldParser = subparsers.add_parser("scaffold", help="Scaffold a new or existing project with Skelebot")
            scaffoldParser.add_argument("-e", "--existing", action='store_true', help="Scaffold an existing project without creating new folder")
        else:
            # Provide Parameters for Skelebot Projects
            self.parser.add_argument("-e", "--env", help="Specify the runtime environment configurations")
            self.parser.add_argument("-s", "--skip-build", action='store_true', help="Skip the build process and attempt to use previous docker build")
            self.parser.add_argument("-n", "--native", action='store_true', help="Run natively instead of through Docker")

        # Add jobs from config to the subparser
        if (config.jobs != None):
            for job in config.jobs:
                subparser = subparsers.add_parser(job.name, help=job.help + " (" + job.source + ")")

                # Add args to the job if they are present in the config
                if (job.args != None):
                    for arg in job.args:
                        if not arg.choices:
                            subparser.add_argument(arg.name)
                        else:
                            subparser.add_argument(arg.name, choices=arg.choices)

                # Add params to the job if they are present in the config
                if (job.params != None):
                    for param in job.params:
                        if param.choices:
                            subparser.add_argument("-" + param.alt, "--" + param.name, choices=param.choices, default=param.default)
                        elif param.isBoolean:
                            subparser.add_argument("-" + param.alt, "--" + param.name, action='store_true', default=param.default)
                        else:
                            subparser.add_argument("-" + param.alt, "--" + param.name, default=param.default)

        # Add the parsers from the active components in the config
        for component in self.config.components:
            subparsers = component.addParsers(subparsers)

    # Construct the Argument Parser based on the config file and parse the args that were passed in
    def parseArgs(self, args=sys.argv[1:]):
        return self.parser.parse_args(args)

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
            description = DESCRIPTION.format(version=VERSION, project=name, desc=description, pVersion=version, env=self.env)

        return description
