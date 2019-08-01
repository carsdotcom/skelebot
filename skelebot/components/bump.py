from ..objects.component import *
from ..systems.generators import yaml

# This component provides the ability to bump the version number in the skelebot.yaml file
class Bump(Component):
    activation = Activation.PROJECT
    commands = ["bump"]

    # Parser for the command that bumps the semantic version in the skelebot.yaml
    def addParsers(self, subparsers):
        helpMessage = "Bump the skelebot.yaml project version"
        parser = subparsers.add_parser("bump", help=helpMessage)
        parser.add_argument("version", help="Select the version number that should be bumped", choices=["major", "minor", "patch"])
        return subparsers

    # Read the current version and bump it based on the version provided (major, minor, or patch) and persist the yaml
    def execute(self, config, args):

        oldVersion = config.version
        mmp = oldVersion.split(".")
        mmp[0] = str(int(mmp[0]) + 1) if (args.version == "major") else mmp[0]
        mmp[1] = str(int(mmp[1]) + 1) if (args.version == "minor") else (mmp[1] if (args.version == "patch") else "0")
        mmp[2] = str(int(mmp[2]) + 1) if (args.version == "patch") else "0"
        version = ".".join(mmp)
        yaml.saveVersion(version)

        print("Bumped " + args.version + " version. v" + oldVersion + " -> v" + version)
