import shutil
import os
import json
from getpass import getpass
import artifactory
import boto3
from schema import Schema, And, Optional, Or
from .artifactRepo import ArtifactRepo
from ...objects.skeleYaml import SkeleYaml
from ...objects.semver import Semver

ARTIFACT_PATH = "{url}/{repo}/{path}/{file}"
AUTH_TYPES = {"user_pass", "token", "apikey"}

class Auth(SkeleYaml):
    """
    Artifactory Specific Authentication Details

    Provides the fields necessary for authenticating with Artifactory.
    """

    schema = Schema({
        Optional('authType'): And(str, Or(*AUTH_TYPES), error="Artifactory Auth 'authType' must be one of: " + ', '.join(AUTH_TYPES)),
        Optional('aws'): And(bool, error="Artifactory Auth 'aws' must be a Boolean"),
        Optional('awsSecret'): And(str, error="Artifactory Auth 'awsSecret' must be a String"),
        Optional('awsProfile'): And(str, error="Artifactory Auth 'awsProfile' must be a String"),
        Optional('awsRegion'): And(str, error="Artifactory Auth 'awsRegion' must be a String"),
    }, ignore_extra_keys=True)

    authType = None
    aws = None
    awsSecret = None
    awsProfile = None
    awsRegion = None

    def __init__(self, authType="user_pass", aws=False, awsSecret="Artifactory", awsProfile=None,
                 awsRegion="us-east-1"):
        """Instantiate the Auth Class Object based on the provided parameters"""
        self.authType = authType
        self.aws = aws
        self.awsSecret = awsSecret
        self.awsProfile = awsProfile
        self.awsRegion = awsRegion

    def loadAwsCredentials(self):
        """Load authentication credentials from AWS Secrets Manager."""
        session = boto3.Session(profile_name=self.awsProfile)
        client = session.client(service_name="secretsmanager", region_name=self.awsRegion)
        return json.loads(client.get_secret_value(SecretId=self.awsSecret)["SecretString"])

    def getUsername(self):
        """ Prompt for an Artifactory username """
        return input("Please provide a valid Artifactory user: ")

    def getToken(self):
        """ Prompt for an Artifactory password/token/apikey """
        cred = "password" if self.authType == "user_pass" else self.authType
        return getpass(f"Please provide a valid Artifactory {cred}: ")

    def getCredentials(self, user=None, token=None):
        """Get authentication credentials either from user input or AWS."""
        if self.aws:
            aws_creds = self.loadAwsCredentials()
            user = aws_creds.get('user', None)
            token = aws_creds.get('token', None)
        else:
            # Obtain any missing credentials
            if (user is None) and (self.authType == "user_pass"):
                user = self.getUsername()
            if (token is None):
                token = self.getToken()

        creds = {}
        if self.authType == "user_pass":
            creds = {"auth": (user, token)}
        elif self.authType == "token":
            creds = {"token": token}
        elif self.authType == "apikey":
            creds = {"apikey": token}

        return creds


class ArtifactoryRepo(ArtifactRepo):
    """
    Artifactory Repository Class

    Contains details and functions for pushing and pulling artifacts from Artifactory
    """

    schema = Schema({
        'url': And(str, error="Artifactory 'url' must be a String"),
        'repo': And(str, error="Artifactory 'repo' must be a String"),
        'path': And(str, error="Artifactory 'path' must be a String"),
        Optional('auth'): And(dict, error="Artifactory 'auth' must be an Object"),
    }, ignore_extra_keys=True)

    url = None
    repo = None
    path = None
    auth = None

    @classmethod
    def load(cls, config):
        """Instantiate the Artifactory Auth Class Object if it is present"""

        cls.validate(config)
        auth = Auth.load(config.get("auth", {}))

        return cls(config.get("url"), config.get("repo"), config.get("path"), auth)

    def __init__(self, url, repo, path, auth=None):
        """ Initialize the values for an Artifactory connection and set the global config """
        self.url = url
        self.repo = repo
        self.path = path
        self.auth = auth or Auth()

    def requiresUsername(self):
        """Check if authentication requires username from user input."""
        return (not self.auth.aws) and (self.auth.authType == "user_pass")

    def requiresToken(self):
        """Check if authentication requires password/token/apikey from user input."""
        return (not self.auth.aws)

    def getLatestCompatibleVersion(self, artifact, currentVersion, creds):
        """ Search for the latest compatible version for the provided version number """

        print("Searching for Latest Compatible Artifact")
        version = None
        currentSemver = Semver(currentVersion)

        listUrl = "{url}/{repo}/{path}/".format(url=self.url, repo=self.repo, path=self.path)
        ext = artifact.file.split(".")[1]
        path = artifactory.ArtifactoryPath(listUrl, **creds)

        # Iterate over all artifacts in the ArtifactoryPath (because path.glob was throwing exceptions on Linux systems)
        if (path.exists()):
            for pathArtifact in path: # Only look at artifacts with the same filename and major version
                modelPrefix = "{filename}_v{major}".format(filename=artifact.name, major=currentSemver.major)
                if modelPrefix in str(pathArtifact):
                    artifactSemver = Semver(str(pathArtifact).split("_v")[1].split(ext)[0])
                    if (currentSemver.isBackwardCompatible(artifactSemver)) and ((version is None) or (version < artifactSemver)):
                        version = artifactSemver # Identify the latest compatible version

        # Raise an error if no compatible version is found
        if (version is None):
            raise RuntimeError(self.ERROR_NOT_COMPATIBLE)

        return version

    def push(self, artifact, version, force=False, user=None, token=None, prefix=None):
        """ Push the artifact with the given version number to Artifactory """

        creds = self.auth.getCredentials(user=user, token=token)

        artifactName = artifact.getVersionedName(version, prefix=prefix)
        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifactName)
        path = artifactory.ArtifactoryPath(url, **creds)

        # Error and exit if artifact already exists and we are not forcing an override
        if (not force) and (path.exists()):
            raise RuntimeError(self.ERROR_ALREADY_PUSHED)

        # Push the artifact to the path in Artifactory
        print("Deploying {file} to {url}".format(file=artifactName, url=url))
        shutil.copyfile(artifact.file, artifactName)
        try:
            path.deploy_file(artifactName)
            os.remove(artifactName)
        except:
            os.remove(artifactName)
            raise

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, token=None):
        """ Pull the artifact with the given version number (or LATEST) from Artifactory """

        creds = self.auth.getCredentials(user=user, token=token)

        # Find Latest Compatible Version or Use Provided Version Number if the artifact is not 'singular'
        version = version if (version != "LATEST" or artifact.singular == True) else self.getLatestCompatibleVersion(artifact, currentVersion, creds)

        # Construct the Artifactory URL for the specified Artifact
        artifactName = artifact.getVersionedName(version)
        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifactName)
        path = artifactory.ArtifactoryPath(url, **creds)

        # Download Artifact from Artifactory and save it to the disk
        if (path.exists()):
            print("Pulling {file} from {url}".format(file=artifactName, url=url))
            with path.open() as fd:
                dest = artifact.file if (override) else artifactName
                with open(dest, "wb") as out:
                    out.write(fd.read())
        else:
            print("Artifact Not Found: {url}".format(url=url))
