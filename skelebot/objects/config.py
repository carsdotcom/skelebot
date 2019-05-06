# The base object for the configurations for a Skelebot project
class Config():
    name = None
    description = None
    version = None
    skelebotVersion = None
    maintainer = None
    contact = None
    langauge = None
    ephemeral = None
    components = None

    # Initialize the object with required values and set the components list to an empty list to start
    def __init__(self, name, description, version, skelebotVersion, maintainer, contact, language, ephemeral, components=[]):
        self.name = name
        self.description = description
        self.version = version
        self.skelebotVersion = skelebotVersion
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.ephemeral = ephemeral
        self.components = components

    def addComponent(self, component):
        components.append(component)

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "description", "version", "skelebotVersion", "maintainer", "contact", "language", "ephemeral", "components"]
