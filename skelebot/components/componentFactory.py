from ..objects.component import Activation
from .plugin import Plugin
from .jupyter import Jupyter
from .kerberos import Kerberos
from .bump import Bump
from .prime import Prime
from .dexec import Dexec

COMPONENTS = {
    Plugin.__name__.lower(): Plugin,
    Jupyter.__name__.lower(): Jupyter,
    Kerberos.__name__.lower(): Kerberos,
    Bump.__name__.lower(): Bump,
    Prime.__name__.lower(): Prime,
    Dexec.__name__.lower(): Dexec
}

def buildComponents(activations=[], ignores=[]):
    components = []
    for component in list(COMPONENTS.values()):
        if (component.activation in activations) and (component.__name__ not in ignores):
            components.append(component())

    return components

def buildComponent(name, data=None):
    return COMPONENTS[name].load(data) if (name in COMPONENTS) else None
