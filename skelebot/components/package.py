"""Package Component"""

import os
from subprocess import call
from schema import Schema, And, Optional
from ..objects.component import Activation, Component

HELP_TEMPLATE = "Package the codebase into a single zip file ({path})"
COMMAND_TEMPLATE = "zip -r {path} .{ignores}"

class Package(Component):
    """
    Package Class

    Provides the ability to package the codebase into a zip file artifact for easy distribution
    """

    activation = Activation.PROJECT
    commands = ["package"]

    schema = Schema({
        'path': And(str, error='Package \'path\' must be a String'),
        Optional('ignores'): And(list, error='Package \'ignores\' must be a List')
    }, ignore_extra_keys=True)

    path = None
    ignores = None

    def __init__(self, path=None, ignores=None):
        """Initialize the class with simple default values for path and ignores"""

        self.path = path
        self.ignores = ignores

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the package command that zips up the codebase
        """

        helpMessage = HELP_TEMPLATE.format(path=self.path)
        subparsers.add_parser("package", help=helpMessage)
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executed when the package command is provided it zips the codebase into a single file
        while ingoring a list of folders and files in the process
        """
        # Ensure we always create a new zipfile
        if os.path.exists(self.path):
            os.remove(self.path)

        ignores = f" -x {' '.join(self.ignores)}" if (self.ignores is not None) else ""
        command = COMMAND_TEMPLATE.format(path=self.path, ignores=ignores)
        return call(command, shell=True)
