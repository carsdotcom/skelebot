from ..objects.component import *
from ..common import SKELEBOT_HOME, PLUGINS_HOME

import os
import zipfile

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
        # Create the ~/.skelebot directory if not already present
        skelebotHome = os.path.expanduser(SKELEBOT_HOME)
        if (os.path.exists(skelebotHome) == False):
            os.makedirs(skelebotHome, exist_ok=True)

        # Create the ~/.skelebot/plugins directory if not already present
        pluginsHome = os.path.expanduser(PLUGINS_HOME)
        if (os.path.exists(pluginsHome) == False):
            os.makedirs(pluginsHome, exist_ok=True)

        # Unzip the plugin into the plugins folder
        zip_ref = zipfile.ZipFile(args.plugin, 'r')
        zip_ref.extractall(pluginsHome)
        zip_ref.close()
