"""Component Factory"""

import os
import sys
import shutil
import importlib
from colorama import Fore, Style
from ..objects.component import Activation
from ..common import PLUGINS_HOME, PLUGINS_QUARANTINE
from .plugin import Plugin
from .jupyter import Jupyter
from .kerberos import Kerberos
from .bump import Bump
from .prime import Prime
from .dexec import Dexec
from .artifactory import Artifactory
from .registry import Registry
from .repository.repository import Repository
from .environments import Environments

WARNING_HEADER = Fore.YELLOW + "WARNING" + Style.RESET_ALL
PLUGIN_WARNING = WARNING_HEADER + " | The {} plugin contains errors - Adding plugin to Quarantine"

class ComponentFactory():
    """
    Component Factory Class

    Maintains and builds all of the components in Skelebot including plugin components installed
    in the Skelebot Home folder
    """

    COMPONENTS = None

    def __init__(self):
        """Initializes the default list of components in Skelebot"""

        self.COMPONENTS = {
            Plugin.__name__.lower(): Plugin,
            Jupyter.__name__.lower(): Jupyter,
            Kerberos.__name__.lower(): Kerberos,
            Bump.__name__.lower(): Bump,
            Prime.__name__.lower(): Prime,
            Dexec.__name__.lower(): Dexec,
            Artifactory.__name__.lower(): Artifactory,
            Registry.__name__.lower(): Registry,
            Repository.__name__.lower(): Repository,
            Environments.__name__.lower(): Environments
        }

        # Add the plugin components to the master list
        pluginsHome = os.path.expanduser(PLUGINS_HOME)
        if (os.path.exists(pluginsHome)):
            sys.path.append(pluginsHome)
            for pluginName in os.listdir(pluginsHome):
                if (pluginName[0] != "_"):
                    try:
                        module = importlib.import_module("{name}.{name}".format(name=pluginName))
                        plugin = getattr(module, pluginName[0].upper() + pluginName[1:])
                        self.COMPONENTS[pluginName.lower()] = plugin
                    except Exception:
                        print(PLUGIN_WARNING.format(pluginName))

                        pluginsQuarantine = os.path.expanduser(PLUGINS_QUARANTINE)
                        if not os.path.exists(pluginsQuarantine):
                            os.makedirs(pluginsQuarantine)

                        src = "{folder}/{name}".format(name=pluginName, folder=pluginsHome)
                        dst = "{folder}/{name}".format(name=pluginName, folder=pluginsQuarantine)
                        shutil.move(src, dst)

    def buildComponents(self, activations=None, ignores=None):
        """Constructs a list of components based on which are active and which should be ignored"""

        activations = activations if activations is not None else [Activation.ALWAYS]
        ignores = ignores if ignores is not None else []
        components = []
        for component in list(self.COMPONENTS.values()):
            if (component.activation in activations) and (component.__name__ not in ignores):
                components.append(component())

        return components

    def buildComponent(self, name, data=None):
        """Builds a single component object based on it's name with the data provided"""

        return self.COMPONENTS[name].load(data) if (name in self.COMPONENTS) else None
