from ..objects.component import *

import os
import zipfile

PLUGIN_FOLDER = os.path.expanduser("~/.skelebot/plugins/")

# This component provides the ability to install plugins into Skelebot at any time
class Plugin(Component):
    activation = Activation.ALWAYS
    commands = ["plugin"]

    # Parser for the command that installs a plugin from a zip file on the hard drive
    def addParsers(self, subparsers):
        parser = subparsers.add_parser("plugin", help="Install a plugin for skelebot from a local zip file")
        parser.add_argument("plugin", help="The zip file of the skelebot plugin")
        return subparsers
    
    # Install the plugin from the zip file specified in the plugin arg
    def execute(self, config, args):
        zip_ref = zipfile.ZipFile(args.plugin, 'r')
        zip_ref.extractall(PLUGIN_FOLDER)
        zip_ref.close()
