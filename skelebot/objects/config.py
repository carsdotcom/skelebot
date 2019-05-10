from .skeleYaml import SkeleYaml

# The base object for the configurations for a Skelebot project
class Config(SkeleYaml):
    name = None
    description = None
    version = None
    skelebotVersion = None
    maintainer = None
    contact = None
    language = None
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

    # Adds extra logic to handle the components coversion to dict since the YAML and Object structures don't exactly match
    def toDict(self):
        dctComp = {}
        for component in self.components:
            componentDct = component.toDict()
            if (componentDct != {}):
                dctComp[component.__class__.__name__.lower()] = componentDct

        dct = super(Config, self).toDict()
        dct["components"] = dctComp
        return dct
