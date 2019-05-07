from .plugin import Plugin

COMPONENTS = {
    "plugin": Plugin
}

def getComponents():
    return list(COMPONENTS.values())

def getComponent(name):
    return COMPONENTS[name] if (name in COMPONENTS) else None
