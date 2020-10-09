"""Repository Component"""

from schema import Schema, And, Optional, SchemaError
from .s3Repo import S3Repo
from .artifactoryRepo import ArtifactoryRepo
from ...objects.component import Activation, Component
from ...objects.skeleYaml import SkeleYaml

ERROR_NOT_COMPATIBLE = "No Compatible Version Found"
ERROR_ALREADY_PUSHED = "This artifact version already exists. Please bump the version or use the force parameter (-f) to overwrite the artifact."

class Artifact(SkeleYaml):
    """
    Artifact Class

    Object contained within a list of the artifactory configuration in order to specify the
    artifact files and artifact names
    """

    VERSIONED_NAME = "{filename}_v{version}.{ext}"
    SINGULAR_NAME = "{filename}.{ext}"

    schema = Schema({
        'name': And(str, error="Artifact 'name' must be a String"),
        'file': And(str, error="Artifact 'file' must be a String"),
        Optional('singular'): And(bool, error="Artifact 'singular' must be a Boolean"),
    }, ignore_extra_keys=True)

    name = None
    file = None
    singular = None

    def __init__(self, name, file, singular=False):
        """ Initialize the Artifact object with a name to be used in commands a file path """
        self.name = name
        self.file = file
        self.singular = singular

    def getVersionedName(self, version):
        """
        Constuct the full versioned filename for the artifact with the given version number
        or without the number if it is a 'singular' artifact instead of a versioned artifact
        """
        ext = self.file.split(".")[1]
        ver_name = None
        if (self.singular):
            ver_name = self.SINGULAR_NAME.format(filename=self.name, ext=ext)
        else:
            ver_name = self.VERSIONED_NAME.format(filename=self.name, version=version, ext=ext)
        return ver_name


class Repository(Component):
    """
    Repository Component Class

    Provides the ability to push and pull artifacts that are defined in the skelebot config
    file to and from Artifactory or S3 based on the project version number
    """

    activation = Activation.CONFIG
    commands = ["push", "pull"]

    schema = Schema({
        Optional('artifacts'): And(list, error="Repository 'artifacts' must be a List"),
        Optional('s3'): And(dict, error="Repository 's3' must be an Object"),
        Optional('artifactory'): And(dict, error="Repository 'artifactory' must be an Object"),
    }, ignore_extra_keys=True)

    artifacts = None
    s3 = None
    artifactory = None

    @classmethod
    def load(cls, config):
        """Instantiate the Repository Class Object based on a config dict"""

        cls.validate(config)

        s3 = None
        artifactory = None
        if ("s3" in config):
            s3 = S3Repo.load(config["s3"])
        elif ("artifactory" in config):
            artifactory = ArtifactoryRepo.load(config["artifactory"])
        else:
            raise SchemaError(None, "Repository must contain 's3' or 'artifactory' config")

        artifactDicts = config["artifacts"]
        artifacts = []
        for artifact in artifactDicts:
            newArtifact = Artifact.load(artifact)
            artifacts.append(newArtifact)

        return cls(artifacts, s3, artifactory)

    def __init__(self, artifacts=None, s3=None, artifactory=None):
        """Instantiate the Repository Class Object based on the provided parameters"""

        self.artifacts = artifacts if artifacts is not None else []
        self.s3 = s3
        self.artifactory = artifactory

    def requiresPassword(self):
        return self.artifactory is not None

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds the parsers for push and pull commands to the SkeleParser to push artifacts
        with the project version and pull artifacts with the provided version number
        """

        artifactNames = ["ALL"]
        for artifact in self.artifacts:
            artifactNames.append(artifact.name)

        repo = "Artifactory" if self.artifactory is not None else "S3"

        parser = subparsers.add_parser("push", help="Push an artifact to {}".format(repo))
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("-f", "--force", action='store_true', help="Force the push")
        if (self.requiresPassword()):
            parser.add_argument("-u", "--user", help="Auth user for Artifactory")
            parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        parser = subparsers.add_parser("pull", help="Pull an artifact from {}".format(repo))
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("version", help="The version of the artifact to pull")
        parser.add_argument("-o", "--override", action='store_true',  help="Override the model in the existing directory")
        if (self.requiresPassword()):
            parser.add_argument("-u", "--user", help="Auth user for Artifactory")
            parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        return subparsers

    def execute(self, config, args, host=None):

        # Obtain the user and token if required
        user = None
        token = None
        if (self.requiresPassword()):
            user = args.user
            token = args.token

        # Obtain the configured artifact repository
        artifactRepo = self.s3 if self.s3 is not None else self.artifactory

        # Obtain the artifact(s) that matches the provided name
        for artifact in self.artifacts:
            if ((args.artifact == artifact.name) | (args.artifact == "ALL")):

                # Push or Pull the Artifact
                if (args.job == "push"): # Push from Disk to Repo
                    print("Pushing version {version} of {artifact}".format(version=config.version, artifact=artifact.name))
                    artifactRepo.push(artifact, config.version, args.force, user, token)
                elif (args.job == "pull"): # Pull from Repo to Disk
                    print("Pulling version {version} of {artifact}".format(version=args.version, artifact=artifact.name))
                    artifactRepo.pull(artifact, args.version, config.version, args.override, user, token)
