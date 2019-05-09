# The base object for the configurations for a Skelebot project
class Config():
    name = None
    description = None
    version = None
    skelebotVersion = None
    maintainer = None
    contact = None
    langauge = None
    primaryJob = None
    ephemeral = None
    dependencies = None
    ignores = None
    jobs = None
    components = None

    # Initialize the object with required values and set the components list to an empty list to start
    def __init__(self, name=None, description=None, version=None, skelebotVersion=None, maintainer=None, contact=None,
                 language=None, primaryJob=None, ephemeral=None, dependencies=[], ignores=[], jobs=[], components=[]):
        self.name = name
        self.description = description
        self.version = version
        self.skelebotVersion = skelebotVersion
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.primaryJob = primaryJob
        self.ephemeral = ephemeral
        self.dependencies = dependencies
        self.ignores = ignores
        self.components = components
        self.jobs = jobs

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "description", "version", "skelebotVersion", "maintainer", "contact", "language", "primaryJob", "ephemeral",
                "dependencies", "ignores", "jobs"]
