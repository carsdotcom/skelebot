import artifactory
import shutil
import os
from schema import Schema, And
from .artifactRepo import ArtifactRepo
from ...objects.semver import Semver

ARTIFACT_PATH = "{url}/{repo}/{path}/{file}"

class ArtifactoryRepo(ArtifactRepo):
    """
    Artifactory Repository Class

    Contains details and functions for pushing and pulling artifacts from Artifactory
    """

    schema = Schema({
        'url': And(str, error="Artifactory 'url' must be a String"),
        'repo': And(str, error="Artifactory 'repo' must be a String"),
        'path': And(str, error="Artifactory 'path' must be a String"),
    }, ignore_extra_keys=True)

    url = None
    repo = None
    path = None

    def __init__(self, url, repo, path):
        """ Initialize the values for an Artifactory connection and set the global config """
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
        """ Prompt for an Artifactory username """
        return input("Please provide a valid Artifactory user: ")

    def getToken(self):
        """ Prompt for an Artifactory token """
        return input("Please provide a valid Artifactory token: ")

    def getLatestCompatibleVersion(self, artifact, currentVersion, user, token):
        """ Search for the latest compatible version for the provided version number """

        print("Searching for Latest Compatible Artifact")
        version = None
        currentSemver = Semver(currentVersion)

        listUrl = "{url}/{repo}/{path}/".format(url=self.url, repo=self.repo, path=self.path)
        ext = artifact.file.split(".")[1]
        path = artifactory.ArtifactoryPath(listUrl, auth=(user, token))

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

    def push(self, artifact, version, force=False, user=None, password=None):
        """ Push the artifact with the given version number to Artifactory """

        # Obtain any missing credentials
        if (user is None):
            user = self.getUsername()
        if (password is None):
            password = self.getToken()

        artifactName = artifact.getVersionedName(version)
        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifactName)

        # Error and exit if artifact already exists and we are not forcing an override
        if (not force) and (artifactory.ArtifactoryPath(url, auth=(user, password)).exists()):
            raise RuntimeError(self.ERROR_ALREADY_PUSHED)

        # Push the artifact to the path in Artifactory
        print("Deploying {file} to {url}".format(file=artifactName, url=url))
        shutil.copyfile(artifact.file, artifactName)
        path = artifactory.ArtifactoryPath(url, auth=(user, password))
        try:
            path.deploy_file(artifactName)
            os.remove(artifactName)
        except:
            os.remove(artifactName)
            raise

    def pull(self, artifact, version, currentVersion=None, override=False, user=None, password=None):
        """ Pull the artifact with the given version number (or LATEST) from Artifactory """

        # Obtain any missing credentials
        if (user is None):
            user = self.getUsername()
        if (password is None):
            password = self.getToken()

        # Find Latest Compatible Version or Use Provided Version Number if the artifact is not 'singular'
        version = version if (version != "LATEST" or artifact.singular == True) else self.getLatestCompatibleVersion(artifact, currentVersion, user, password)

        # Construct the Artifactory URL for the specified Artifact
        artifactName = artifact.getVersionedName(version)
        url = ARTIFACT_PATH.format(url=self.url, repo=self.repo, path=self.path, file=artifactName)

        # Download Artifact from Artifactory and save it to the disk
        if (artifactory.ArtifactoryPath(url, auth=(user, password)).exists()):
            print("Pulling {file} from {url}".format(file=artifactName, url=url))
            path = artifactory.ArtifactoryPath(url, auth=(user, password))
            with path.open() as fd:
                dest = artifact.file if (override) else artifactName
                with open(dest, "wb") as out:
                    out.write(fd.read())
        else:
            print("Artifact Not Found: {url}".format(url=url))
