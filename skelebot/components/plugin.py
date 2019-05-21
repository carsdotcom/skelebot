from ..objects.component import *
from ..systems.scaffolding.prompt import promptUser

import os
import sys
import importlib
import zipfile

PLUGIN_FOLDER = os.path.expanduser("~/.skelebot/plugins/")

# This component provides the ability to install plugins into a Skelebot install at any time
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

    # Loop over each plugin form the PLUGIN_FOLDER and execute the scaffold function
    def scaffold():
        plugins = []
        for plugin in os.listdir(PLUGIN_FOLDER):
            pluginComponent = importlib.import_module(PLUGIN_FOLDER + plugin)
            plugins.append(pluginComponent.scaffold())

        return plugins

    #def pluginCommand(config, pluginName):
        #sys.path.append(PLUGIN_FOLDER)
        #module = pluginName + COMMAND_FILE
        #plugin = importlib.import_module(module)
        #pluginConfig = {}
        #for pluginCfg in config.plugins:
        #if (pluginCfg.name == pluginName):
        #pluginConfig = pluginCfg
        #return plugin.command(config, pluginConfig.config) 
