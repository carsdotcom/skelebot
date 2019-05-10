from .plugin import Plugin
from .jupyter import Jupyter

COMPONENTS = {
    Plugin.__name__.lower(): Plugin,
    Jupyter.__name__.lower(): Jupyter
}

def buildComponents(activations=[], ignores=[]):
    components = []
    for component in list(COMPONENTS.values()):
        if (component.activation in activations) and (component.__name__ not in ignores):
            components.append(component())

    return components

def buildComponent(name, data=None):
    return COMPONENTS[name].load(data) if (name in COMPONENTS) else None
