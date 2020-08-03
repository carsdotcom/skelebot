"""Bump Component"""

from ..objects.component import Activation, Component
from ..systems.generators import yaml

MAJOR = "major"
MINOR = "minor"
PATCH = "patch"

class Bump(Component):
    """
    Bump Class

    Provides the ability to bump the major, minor, or patch version of a project based on Semantic
    Versioning standards with the 'bump' command
    """
    activation = Activation.PROJECT
    commands = ["bump"]

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the bump command that takes in a single argument called version to define
        whether it should bump the major, minor, or patch version of the project
        """

        helpMessage = "Bump the skelebot.yaml project version"
        argHelp = "Select the version number that should be bumped"

        parser = subparsers.add_parser("bump", help=helpMessage)
        parser.add_argument("version", help=argHelp, choices=[MAJOR, MINOR, PATCH])

        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executes when the bump command is provided and bumps either the major, minor, or patch
        version of the project depending on which was provided in the command
        """

        oldVersion = config.version
        version = args.version
        mmp = oldVersion.split(".")
        mmp[0] = str(int(mmp[0])+1) if version == MAJOR else mmp[0]
        mmp[1] = str(int(mmp[1])+1) if version == MINOR else (mmp[1] if version == PATCH else "0")
        mmp[2] = str(int(mmp[2])+1) if version == PATCH else "0"
        version = ".".join(mmp)
        yaml.saveVersion(version)

        print("Bumped " + version + " version. v" + oldVersion + " -> v" + version)
