from ..objects.component import Activation
from ..common import SKELEBOT_HOME, PLUGINS_HOME
from .plugin import Plugin
from .jupyter import Jupyter
from .kerberos import Kerberos
from .bump import Bump
from .prime import Prime
from .dexec import Dexec
from .artifactory import Artifactory

import os
import sys
import importlib

class ComponentFactory():

    COMPONENTS = None

    def __init__(self):
        self.COMPONENTS = {
            Plugin.__name__.lower(): Plugin,
            Jupyter.__name__.lower(): Jupyter,
            Kerberos.__name__.lower(): Kerberos,
            Bump.__name__.lower(): Bump,
            Prime.__name__.lower(): Prime,
            Dexec.__name__.lower(): Dexec,
            Artifactory.__name__.lower(): Artifactory
        }

        # Add the plugin components to the master list
        pluginsHome = os.path.expanduser(PLUGINS_HOME)
        if (os.path.exists(pluginsHome)):
            sys.path.append(pluginsHome)
            for pluginName in os.listdir(pluginsHome):
                if (pluginName[0] != "_"):
                    module = importlib.import_module("{name}.{name}".format(name=pluginName))
                    plugin = getattr(module, pluginName[0].upper() + pluginName[1:])
                    self.COMPONENTS[pluginName.lower()] = plugin

    def buildComponents(self, activations=[], ignores=[]):
        components = []
        for component in list(self.COMPONENTS.values()):
            if (component.activation in activations) and (component.__name__ not in ignores):
                components.append(component())

        return components

    def buildComponent(self, name, data=None):
        return self.COMPONENTS[name].load(data) if (name in self.COMPONENTS) else None
