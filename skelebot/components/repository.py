"""Repository Component"""

import os
import shutil
import artifactory
import s3fs
from deprecated import deprecated
from requests.exceptions import MissingSchema
from schema import Schema, And, Optional, SchemaError
from ..common import DEPRECATION_WARNING
from ..objects.component import Activation, Component
from ..objects.skeleYaml import SkeleYaml
from ..objects.semver import Semver

ERROR_NOT_COMPATIBLE = "No Compatible Version Found"
ERROR_ALREADY_PUSHED = "This artifact version already exists. Please bump the version or use the force parameter (-f) to overwrite the artifact."

class Artifact(SkeleYaml):
    """
    Artifact Class

    Object contained within a list of the artifactory configuration in order to specify the
    artifact files and artifact names
    """

    VERSIONED_NAME = "{filename}_v{version}.{ext}"

    schema = Schema({
        'name': And(str, error='Artifact \'name\' must be a String'),
        'file': And(str, error='Artifact \'file\' must be a String'),
    }, ignore_extra_keys=True)

    name = None
    file = None

    def __init__(self, name, file):
        self.name = name
        self.file = file

    def getVersionedName(self, version):
        ext = self.file.split(".")[1]
        return self.VERSIONED_NAME.format(filename=self.name, version=version, ext=ext)

class ArtifactRepo(SkeleYaml):
    """
    Artifact Repo Interface

    Defines the essential functions for an Artifact Repo to implement
    """

    def push(self, artifact, force=False, user=None, password=None):
        pass

    def pull(self, artifact, version, override=False, user=None, password=None):
        pass

    def list(self, artifact, ext, user=None, password=None):
        pass

class S3fsRepo(ArtifactRepo):
    """
    S3 File System Class

    S3 connection details for saving artifacts in AWS S3 buckets
    """

    schema = Schema({
        'bucket': And(str, error='S3fs \'bucket\' must be a String'),
        'region': And(str, error='S3fs \'region\' must be a String'),
        Optional('profile'): And(str, error='S3fs \'profile\' must be a String'),
    }, ignore_extra_keys=True)

    bucket = None
    region = None
    profile = None

    def __init__(self, bucket, region, profile):
        self.bucket = bucket
        self.region = region
        self.profile = profile

    def push(self, artifact, force=False, user=None, password=None):
        pass # TODO

    def pull(self, artifact, version, override=False, user=None, password=None):
        pass # TODO

    def list(self, artifact, user=None, password=None):
        pass # TODO

class ArtifactoryRepo(ArtifactRepo):
    """
    Artifactory Repository Class

    Contains details and functions for pushing and pulling artifacts from Artifactory
    """

    ARTIFACT_PATH = "{url}/{repo}/{path}/{file}"

    schema = Schema({
        'url': And(str, error='Artifactory \'url\' must be a String'),
        'repo': And(str, error='Artifactory \'repo\' must be a String'),
        'path': And(str, error='Artifactory \'path\' must be a String'),
    }, ignore_extra_keys=True)

    url = None
    repo = None
    path = None

    def __init__(self, url, repo, path):
        self.url = url
        self.repo = repo
        self.path = path

        artifactory.global_config = {
            self.url: {
                'username': None,
                'verify': True,
                'cert': None,
                'password': None
            }
        }

    def getUsername(self):
        return input("Please provide a valid Artifactory user: ")

    def getToken(self):
        return input("Please provide a valid Artifactory token: ")

    def push(self, artifact, force=False, user=None, password=None):

        # Obtain any missing credentials
        if (user is None):
            user = self.getUsername()
        if (password is None):
            password = self.getToken()

        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifact)

        # Error and exit if artifact already exists and we are not forcing an override
        try:
            if (not force) and (artifactory.ArtifactoryPath(url, auth=(user, password)).exists()):
                raise RuntimeError(ERROR_ALREADY_PUSHED)
        except MissingSchema:
            pass

        # Push the artifact to the path in Artifactory
        print("Deploying {file} to {url}".format(file=artifact, url=url))
        path = artifactory.ArtifactoryPath(url, auth=(user, password))
        path.deploy_file(artifact)

    def pull(self, artifact, version, override=False, user=None, password=None):

        # Obtain any missing credentials
        if (user is None):
            user = self.getUsername()
        if (password is None):
            password = self.getToken()

        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifact)

        if (artifactory.ArtifactoryPath(url, auth=(user, password)).exists()):
            print("Pulling {file} from {url}".format(file=artifact, url=url))
            path = artifactory.ArtifactoryPath(url, auth=(user, password))
            with path.open() as fd:
                dest = original if (override) else artifact
                with open(dest, "wb") as out:
                    out.write(fd.read())
        else:
            print("Artifact Not Found: {url}".format(url=url))

    def list(user, token, url, filename, ext): # TODO
        """Searches the artifact folder to find the latest compatible artifact version"""

        print("Searching for Latest Compatible Artifact")
        compatibleSemver = None
        currentSemver = Semver(currentVersion)

        # Find the artifacts in the folder with the same name and major version
        path = artifactory.ArtifactoryPath(listUrl, auth=(user, token))
        if (path.exists()):
            pathGlob = "{filename}_v{major}.*.{ext}".format(filename=filename, ext=ext, major=currentSemver.major)
            for artifact in path.glob(pathGlob):
                artifactSemver = Semver(str(artifact).split("_v")[1].split(ext)[0])

                # Identify the latest compatible version
                if (currentSemver.isBackwardCompatible(artifactSemver)) and ((compatibleSemver is None) or (compatibleSemver < artifactSemver)):
                    compatibleSemver = artifactSemver

        # Raise an error if no compatible version is found
        if (compatibleSemver is None):
            raise RuntimeError(ERROR_NOT_COMPATIBLE)

        return "{filename}_v{version}.{ext}".format(filename=filename, version=compatibleSemver, ext=ext)

class Repository(Component):
    """
    Repository Component Class

    Provides the ability to push and pull artifacts that are defined in the skelebot config
    file to and from Artifactory or S3 based on the project version number
    """

    activation = Activation.CONFIG
    commands = ["push", "pull"]

    schema = Schema({
        Optional('artifacts'): And(list, error='Repository \'artifacts\' must be a List'),
        Optional('s3fs'): And(dict, error='Repository \'s3fs\' must be an Object'),
        Optional('artifactory'): And(dict, error='Repository \'artifactory\' must be an Object'),
    }, ignore_extra_keys=True)

    artifacts = None
    s3fs = None
    artifactory = None

    @classmethod
    def load(cls, config):
        """Instantiate the Repository Class Object based on a config dict"""

        cls.validate(config)

        s3fs = None
        artifactory = None
        if ("s3fs" in config)
            s3fs = S3fs.load(config["s3fs"])
        elif ("artifactory" in config)
            artifactory = Artifactory.load(config["s3fs"])
        else:
            raise SchemaError(None, "Repository must contain 's3fs' or 'artifactory' config")

        artifactDicts = config["artifacts"]
        artifacts = []
        for artifact in artifactDicts:
            newArtifact = Artifact.load(artifact)
            artifacts.append(newArtifact)

        return cls(artifacts, s3fs, artifactory)

    def __init__(self, artifacts=None, s3fs=None, artifactory=None):
        """Instantiate the Repository Class Object based on the provided parameters"""

        self.artifacts = artifacts if artifacts is not None else []
        self.s3fs = s3fs
        self.artifactory = artifactory

    def requiresPassword(self):
        return self.artifactory is not None

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds the parsers for push and pull commands to the SkeleParser to push artifacts
        with the project version and pull artifacts with the provided version number
        """

        artifactNames = []
        for artifact in self.artifacts:
            artifactNames.append(artifact.name)

        parser = subparsers.add_parser("push", help="Push an artifact to artifactory")
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("-f", "--force", action='store_true', help="Force the push")
        if (self.requiresPassword()):
            parser.add_argument("-u", "--user", help="Auth user for Artifactory")
            parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        parser = subparsers.add_parser("pull", help="Pull an artifact from artifactory")
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("version", help="The version of the artifact to pull")
        parser.add_argument("-o", "--override", action='store_true',  help="Override the model in the existing directory")
        if (self.requiresPassword()):
            parser.add_argument("-u", "--user", help="Auth user for Artifactory")
            parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        return subparsers

    def execute(self, config, args):

        # Obtain the artifact that matches the provided name
        selectedArtifact = None
        for artifact in self.artifacts:
            if (artifact.name == args.artifact):
                selectedArtifact = artifact

        ext = selectedArtifact.file.split(".")[1]

        # Construct the full verioned name of the artifact
        version = config.version if (args.job == "push") else args.version
        artifact = selectedArtifact.getVersionedName(version)

        # Obtain the configured artifact repository
        artifactRepo = self.s3fs if self.s3fs is not None else self.artifactory

        if (args.job == "push"):
            # PUSH - Copy artifact to new version name, push the artifact, and remove the temp file
            try:
                shutil.copyfile(selectedArtifact.file, artifact)
                artifactRepo.push(artifact, args.force, args.user, args.token)
                os.remove(artifact)
            except:
                os.remove(artifact)
                raise
        elif (args.job == "pull"):
            # PULL - Pull the provided version of the artifact or the Latest Compatible Version
            if (args.version == "LATEST"):
                #TODO: Get LCV
            artifactRepo.pull(artifact, args.version, args.override, args.user, args.token)


    def executeS3FS(self, config, args, selectedArtifact, ext, version):
        fs = s3fs.S3FileSystem(region_name=self.region, profile_name=self.profile)

        print("Reading Files in Bucket: {}".format(s3_input))
        for filename in fs.ls(s3_input):
            if (filename.endswith(".parquet")):
                print("Reading Part: {}".format(filename))
                part = pq.ParquetDataset('s3://' + filename, filesystem=fs).read_pandas().to_pandas()
                parts.append(part)

    def executeArtifactory(self, config, args, selectedArtifact, ext, version):
        """
        Execution Hook

        Executes either the push or pull command depending on which one was provided to push
        the to the repositroy
        """

        # Generate the local artifact file and the final Artifactory url path
        file = None
        if (version == "LATEST"):
            listUrl = "{url}/{repo}/{path}/"
            listUrl = listUrl.format(url=self.url, repo=self.repo, path=self.path)
            file = findCompatibleArtifact(user, token, listUrl, config.version, selectedArtifact.name, ext)
        else:
            file = "{filename}_v{version}.{ext}"
            file = file.format(filename=selectedArtifact.name, version=version, ext=ext)

        url = "{url}/{repo}/{path}/{file}"
        url = url.format(url=self.url, repo=self.repo, path=self.path, file=file)

        # Push the artifact with the config version, or pull with the arg version
        if (args.job == "push"):
            pushArtifact(selectedArtifact.file, user, token, file, url, args.force)
        elif (args.job == "pull"):
            pullArtifact(user, token, file, url, args.override, selectedArtifact.file)
