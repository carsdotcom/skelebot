from ..objects.component import *

class Plugin(Component):
    activation = Activation.ALWAYS

    # Parser for the command that installs a plugin from a zip file on the hard drive
    def addParsers(self, subparsers):
        parser = subparsers.add_parser("plugin", help="Install a plugin for skelebot from a local zip file")
        parser.add_argument("plugin", help="The zip file of the skelebot plugin")
        return subparsers
