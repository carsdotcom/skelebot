"""Root Config Class for Skelebot YAML File"""

from .skeleYaml import SkeleYaml
from ..common import LANGUAGE_IMAGE

class Config(SkeleYaml):
    """
    Root Config Class for Skelebot YAML File

    Built on top of the SkeleYaml parent Object in order to enherit and extend the functionality
    of yaml file generation and parsing
    """

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

    def __init__(self, name=None, description=None, version=None, maintainer=None, contact=None,
                 language=None, baseImage=None, primaryJob=None, ephemeral=None, dependencies=None,
                 ignores=None, jobs=None, ports=None, components=None, params=None):
        """Initialize the config object with all provided optional attributes"""

        self.name = name
        self.description = description
        self.version = version
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.baseImage = baseImage
        self.primaryJob = primaryJob
        self.ephemeral = ephemeral
        self.dependencies = dependencies if dependencies is not None else []
        self.ignores = ignores if ignores is not None else []
        self.jobs = jobs if jobs is not None else []
        self.ports = ports if ports is not None else []
        self.components = components if components is not None else []
        self.params = params if params is not None else []

    def toDict(self):
        """
        Extends the parent function in order to logic for handling the conversion of
        components since the Class structure and yaml sctructures do not match
        """

        components_dict = {}
        for component in self.components:
            component_dict = component.toDict()
            if component_dict != {}:
                components_dict[component.__class__.__name__.lower()] = component_dict

        dct = super().toDict()
        dct["components"] = components_dict
        return dct

    def getBaseImage(self):
        """
        Returns the proper base image based on the values for language and kerberos,
        or returns the user defined base image if provided in the config yaml
        """

        if self.baseImage:
            image = self.baseImage
        else:
            language = self.language if self.language is not None else "NA"
            image = LANGUAGE_IMAGE[language]

            variant = "base"
            for component in self.components:
                if component.__class__.__name__.lower() == "kerberos":
                    variant = "krb"

            image = image[variant]

        return image

    def getImageName(self):
        """Construct and return the name for the docker image based on the project name"""
        return self.name.lower().replace(" ", "-")
