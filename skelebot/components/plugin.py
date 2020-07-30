"""Plugin Component"""

import os
import zipfile
from ..objects.component import Activation, Component
from ..common import SKELEBOT_HOME, PLUGINS_HOME

class Plugin(Component):
    """
    Plugin Class

    Provides the ability to install plugins into Skelebot at any time
    """

    activation = Activation.ALWAYS
    commands = ["plugin"]

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Add parser for the plugin command that installs a plugin from a zip file on the hard drive
        """

        helpMessage = "Install a plugin for skelebot from a local zip file"
        parser = subparsers.add_parser("plugin", help=helpMessage)
        parser.add_argument("plugin", help="The zip file of the skelebot plugin")
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        When the plugin command is provided the plugin from the zip file specified in the plugin
        argument is installed in the Skelebot Plugins folder inside Skelebot Home
        """

        # Create the ~/.skelebot directory if not already present
        skelebotHome = os.path.expanduser(SKELEBOT_HOME)
        if (os.path.exists(skelebotHome) is False):
            os.makedirs(skelebotHome, exist_ok=True)

        # Create the ~/.skelebot/plugins directory if not already present
        pluginsHome = os.path.expanduser(PLUGINS_HOME)
        if (os.path.exists(pluginsHome) is False):
            os.makedirs(pluginsHome, exist_ok=True)

        # Unzip the plugin into the plugins folder
        zip_ref = zipfile.ZipFile(args.plugin, 'r')
        zip_ref.extractall(pluginsHome)
        zip_ref.close()
