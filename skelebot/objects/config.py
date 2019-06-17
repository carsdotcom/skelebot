from .skeleYaml import SkeleYaml
from ..common import IMAGE_VERSION, LANGUAGE_IMAGE

# The base object for the configurations for a Skelebot project
class Config(SkeleYaml):
    name = None
    description = None
    version = None
    maintainer = None
    contact = None
    language = None
    primaryJob = None
    ephemeral = None
    dependencies = None
    ignores = None
    jobs = None
    ports = None
    components = None

    # Initialize the object with required values and set the components list to an empty list to start
    def __init__(self, name=None, description=None, version=None, maintainer=None, contact=None,
                 language=None, primaryJob=None, ephemeral=None, dependencies=[], ignores=[], jobs=[], ports=[], components=[]):
        self.name = name
        self.description = description
        self.version = version
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.primaryJob = primaryJob
        self.ephemeral = ephemeral
        self.dependencies = dependencies
        self.ignores = ignores
        self.jobs = jobs
        self.ports = ports
        self.components = components

    # Adds extra logic to handle the components coversion to dict since the YAML and Object structures don't exactly match
    def toDict(self):
        dctComp = {}
        for component in self.components:
            componentDct = component.toDict()
            if (componentDct != {}):
                dctComp[component.__class__.__name__.lower()] = componentDct

        dct = super().toDict()
        dct["components"] = dctComp
        return dct

    # Returns the proper base image based on the values for language, kerberos, and version in the project config
    def getBaseImage(self):
        return LANGUAGE_IMAGE[self.language].format(version=IMAGE_VERSION)

    def getImageName(self):
        return self.name.lower().replace(" ", "-")
