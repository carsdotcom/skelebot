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

    # Initialize the parser with the given config and environment
    def __init__(self, config=None, env=None):
        self.config = config
        self.env = env
        self.desc = self.buildDescription()

        # ---Standard Parser Setup---

        # Construct the root argument parser from which all sub-parsers will be built
        self.parser = argparse.ArgumentParser(description=self.desc, formatter_class=argparse.RawTextHelpFormatter)
        subparsers = self.parser.add_subparsers(dest="job")

        if (config.name is None):
            # Add SCAFFOLD parser
            scaffoldParser = subparsers.add_parser("scaffold", help="Scaffold a new or existing project with Skelebot")
            scaffoldParser.add_argument("-e", "--existing", action='store_true', help="Scaffold an existing project without creating new folder")
        else:
            # Add STANDARD PARAMS
            self.parser.add_argument("-e", "--env", help="Specify the runtime environment configurations")
            self.parser.add_argument("-s", "--skip-build", action='store_true', help="Skip the build process and attempt to use previous docker build")
            self.parser.add_argument("-n", "--native", action='store_true', help="Run natively instead of through Docker")

        # ---Config Based Parser Setup---

        # Add JOBS
        if (config.jobs != None):
            for job in config.jobs:
                subparser = subparsers.add_parser(job.name, help=job.help + " (" + job.source + ")")

                # Add ARGS and PARAMS
                subparser = self.addArgs(job.args, subparser)
                subparser = self.addParams(job.params, subparser)
                subparser = self.addParams(config.params, subparser)

        # Add COMPONENT parsers
        for component in self.config.components:
            subparsers = component.addParsers(subparsers)

    # Parse the args from the parser built by the config
    def parseArgs(self, args=sys.argv[1:]):
        return self.parser.parse_args(args)

    # Display the help message from the internal parser object
    def showHelp(self):
        return self.parser.print_help()

    # Add args to the given subparser
    def addArgs(self, args, subparser):
        if (args != None):
            for arg in args:
                if not arg.choices:
                    subparser.add_argument(arg.name, help=arg.help)
                else:
                    subparser.add_argument(arg.name, choices=arg.choices, help=arg.help)
        return subparser

    # Add params to the given subparser
    def addParams(self, params, subparser):
        if (params != None):
            for param in params:
                flags = ["--{}".format(param.name)]
                if (param.alt is not None):
                    flags.append("-{}".format(param.alt))

                if param.choices:
                    subparser.add_argument(*flags, choices=param.choices, default=param.default, help=param.help)
                elif param.accepts == "boolean":
                    subparser.add_argument(*flags, action='store_true', help=param.help)
                elif param.accepts == "list":
                    subparser.add_argument(*flags, nargs='*', default=param.default, help=param.help)
                else:
                    subparser.add_argument(*flags, default=param.default, help=param.help)
        return subparser

    # Construct the description text for the '--help' output
    def buildDescription(self):
        description = "Skelebot Version: {version}".format(version=VERSION)
        if (self.config.name != None):
            name = " ".join([word.capitalize() for word in self.config.name.split("-")])
            description = self.config.description
            version = self.config.version
            description = DESCRIPTION.format(version=VERSION, project=name, desc=description, pVersion=version, env=self.env)

        return description
