"""SkeleParser"""

import sys
import argparse
from ...common import DESCRIPTION
from ...common import VERSION

SCF_ARG = "scaffold"
SCF_HELP = "Scaffold a new or existing project with Skelebot"
SCF_EX = "--existing"
SCF_EX_ALT = "-e"
SCF_EX_HELP = "Scaffold an existing project without creating new folder"

ENV_ARG = "--env"
ENV_ALT = "-e"
ENV_HELP = "Specify the runtime environment configurations"

SB_DST = "skip_build_global"
SB_ARG = "--skip-build"
SB_ALT = "-s"
SB_HELP = "Skip the build process and attempt to use previous docker build"

HS_DST = "host"
HS_ARG = "--docker-host"
HS_ALT = "-d"
HS_HELP = "Set the Docker Host on which the command will be executed"

NT_DST = "native_global"
NT_ARG = "--native"
NT_ALT = "-n"
NT_HELP = "Run natively instead of through Docker"

VN_DST = "version_global"
VN_ARG = "--version"
VN_ALT = "-v"
VN_HELP = "Display the version number of Skelebot"

CN_DST = "contact_global"
CN_ARG = "--contact"
CN_ALT = "-c"
CN_HELP = "Display the contact email of the Skelebot project"

VB_DST = "verbose_global"
VB_ARG = "--verbose"
VB_ALT = "-V"
VB_HELP = "Print all job commands to the screen just before execution"

def addArgs(args, subparser):
    """Add args to the given subparser"""

    if (args is not None):
        for arg in args:
            if not arg.choices:
                subparser.add_argument(arg.name, help=arg.help)
            else:
                subparser.add_argument(arg.name, choices=arg.choices, help=arg.help)
    return subparser

def addParams(params, subparser):
    """Add params to the given subparser"""

    if (params is not None):
        for param in params:
            flags = ["--{}".format(param.name)]
            if (param.alt is not None):
                flags.append("-{}".format(param.alt))

            if param.choices:
                subparser.add_argument(*flags, choices=param.choices, default=param.default,
                                       help=param.help)
            elif param.accepts == "boolean":
                subparser.add_argument(*flags, action='store_true', help=param.help)
            elif param.accepts == "list":
                subparser.add_argument(*flags, nargs='*', default=param.default,
                                       help=param.help)
            else:
                subparser.add_argument(*flags, default=param.default, help=param.help)
    return subparser

class SkeleParser:
    """
    SkeleParser Class

    A wrapper around the argparse that constructs the interface to Skelebot based on the user's
    skelebot.yaml configuration file
    """

    parser = None
    config = None
    env = None
    desc = None

    # Initialize the parser with the given config and environment
    def __init__(self, config=None, env=None):
        """Initialize the argparse Parser based on the Config data if it is present"""

        self.config = config
        self.env = env
        self.desc = self.buildDescription()

        # ---Standard Parser Setup---

        # Construct the root argument parser from which all sub-parsers will be built
        formatter = argparse.RawTextHelpFormatter
        self.parser = argparse.ArgumentParser(description=self.desc, formatter_class=formatter)
        self.parser.add_argument(VN_ALT, VN_ARG, help=VN_HELP, action='store_true', dest=VN_DST)
        subparsers = self.parser.add_subparsers(dest="job")

        if (config.name is None):
            # Add SCF parser
            scaffoldParser = subparsers.add_parser(SCF_ARG, help=SCF_HELP)
            scaffoldParser.add_argument(SCF_EX_ALT, SCF_EX, action='store_true', help=SCF_EX_HELP)
        else:
            # Add STANDARD PARAMS
            self.parser.add_argument(ENV_ALT, ENV_ARG, help=ENV_HELP)
            self.parser.add_argument(HS_ALT, HS_ARG, help=HS_HELP, dest=HS_DST)
            self.parser.add_argument(SB_ALT, SB_ARG, help=SB_HELP, action='store_true', dest=SB_DST)
            self.parser.add_argument(NT_ALT, NT_ARG, help=NT_HELP, action='store_true', dest=NT_DST)
            self.parser.add_argument(CN_ALT, CN_ARG, help=CN_HELP, action='store_true', dest=CN_DST)
            self.parser.add_argument(VB_ALT, VB_ARG, help=VB_HELP, action='store_true', dest=VB_DST)

        # ---Config Based Parser Setup---

        # Add JOBS
        if (config.jobs is not None):
            for job in config.jobs:
                subparser = subparsers.add_parser(job.name, help=job.help + " ("+job.source+")")

                # Add ARGS and PARAMS
                subparser = addArgs(job.args, subparser)
                subparser = addParams(job.params, subparser)
                subparser = addParams(config.params, subparser)

        # Add COMPONENT parsers
        for component in self.config.components:
            subparsers = component.addParsers(subparsers)

    def parseArgs(self, args=None):
        """Parse the args from the parser built by the config"""
        return self.parser.parse_args(args if args is not None else sys.argv[1:])

    def showHelp(self):
        """Display the help message from the internal parser object"""
        self.parser.print_help()

    def buildDescription(self):
        """Construct the description text for the '--help' output"""

        description = "Skelebot Version: {version}".format(version=VERSION)
        if (self.config.name is not None):
            name = " ".join([word.capitalize() for word in self.config.name.split("-")])
            description = self.config.description
            version = self.config.version
            description = DESCRIPTION.format(version=VERSION, project=name, desc=description,
                                             pVersion=version, env=self.env)

        return description
