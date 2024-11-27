"""Package Component"""

from schema import Schema, And, Optional
from subprocess import call
from ..objects.component import Activation, Component

HELP_TEMPLATE = "Package the codebase into a single zip file ({path}.zip)"
COMMAND_TEMPLATE = "zip -r {path}.zip . -x {ignores}"

class Package(Component):
    """
    Package Class

    Provides the ability to package the codebase into a zip file artifact for easy distribution
    """

    activation = Activation.PROJECT
    commands = ["package"]

    schema = Schema({
        'path': And(str, error='Package \'path\' must be an String'),
        Optional('ignores'): And(list, error='Package \'ignores\' must be a List')
    }, ignore_extra_keys=True)

    path = None
    ignores = None

    def __init__(self, path=None, ignores=None):
        """Initialize the class with simple default values for path and ignores"""

        self.path = path
        self.ignores = ignores if (ignores is not None) else []

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the package command that zips up the codebase
        """

        helpMessage = HELP_TEMPLATE.format(name=self.name)
        subparsers.add_parser("package", help=helpMessage)
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executed when the package command is provided it zips the codebase into a single file
        while ingoring a list of folders and files in the process
        """

        command = COMMMAND_TEMPLATE.format(path=self.path, ignores=" ".join(self.ignores))
        return call(command, shell=True)
