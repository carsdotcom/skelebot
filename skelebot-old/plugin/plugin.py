import os
import sys
import importlib
import zipfile

PLUGIN_FOLDER = os.path.expanduser("~/.skelebot/plugins/")
SCAFFOLD_FILE = ".scaffold"
COMMAND_FILE  = ".command"

def installPlugin(pluginFile):
    zip_ref = zipfile.ZipFile(pluginFile, 'r')
    zip_ref.extractall(PLUGIN_FOLDER)
    zip_ref.close()

def pluginScaffold(pluginName):
    sys.path.append(PLUGIN_FOLDER)
    module = pluginName + SCAFFOLD_FILE
    plugin = importlib.import_module(module)
    return plugin.scaffold()

def pluginCommand(config, pluginName):
    sys.path.append(PLUGIN_FOLDER)
    module = pluginName + COMMAND_FILE
    plugin = importlib.import_module(module)
    pluginConfig = {}
    for pluginCfg in config.plugins:
        if (pluginCfg.name == pluginName):
            pluginConfig = pluginCfg
    return plugin.command(config, pluginConfig.config)
