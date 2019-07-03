from .skeleYaml import SkeleYaml
from ..common import LANGUAGE_IMAGE

# The base object for the configurations for a Skelebot project
class Config(SkeleYaml):
    name = None
    description = None
    version = None
    maintainer = None
    contact = None
    language = None
    baseImage = None
    primaryJob = None
    ephemeral = None
    dependencies = None
    ignores = None
    jobs = None
    ports = None
    components = None
    params = None

    # Initialize the object with required values and set the components list to an empty list to start
    def __init__(self, name=None, description=None, version=None, maintainer=None, contact=None, language=None, baseImage=None,
                 primaryJob=None, ephemeral=None, dependencies=[], ignores=[], jobs=[], ports=[], components=[], params=[]):
        self.name = name
        self.description = description
        self.version = version
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.baseImage = baseImage
        self.primaryJob = primaryJob
        self.ephemeral = ephemeral
        self.dependencies = dependencies
        self.ignores = ignores
        self.jobs = jobs
        self.ports = ports
        self.components = components
        self.params = params

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

    # Returns the proper base image based on the values for language and kerberos, or returns the user defined base image
    def getBaseImage(self):

        if (self.baseImage):
            image = self.baseImage
        else:
            language = self.language if self.language != None else "NA"
            image = LANGUAGE_IMAGE[language]

            variant = "base"
            for component in self.components:
                if (component.__class__.__name__.lower() == "kerberos"):
                    variant = "krb"

            image = image[variant]

        return image

    def getImageName(self):
        return self.name.lower().replace(" ", "-")
