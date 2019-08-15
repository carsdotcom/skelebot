"""Artifactory Component"""

import os
import shutil
import artifactory
from requests.exceptions import MissingSchema
from schema import Schema, And, Optional
from ..objects.component import Activation, Component
from ..objects.skeleYaml import SkeleYaml

ERROR_ALREADY_PUSHED = """This artifact version has already been pushed.
Please bump the version before pushing (skelebot bump) or force push (-f)."""

def pushArtifact(artifactFile, user, token, file, url, force):
    """Pushes the given file to the url with the provided user/token auth"""

    # Error and exit if artifact already exists and we are not forcing an override
    try:
        if (not force) and (artifactory.ArtifactoryPath(url, auth=(user, token)).exists()):
            raise Exception(ERROR_ALREADY_PUSHED)
    except MissingSchema:
        pass

    # Rename artifact, deploy the renamed artifact, and then rename it back to original name
    print("Deploying {file} to {url}".format(file=file, url=url))
    path = artifactory.ArtifactoryPath(url, auth=(user, token))
    shutil.copyfile(artifactFile, file)
    try:
        path.deploy_file(file)
        os.remove(file)
    except:
        os.remove(file)
        raise

def pullArtifact(user, token, file, url):
    """Pulls the given file from the url with the provided user/token auth"""

    if (artifactory.ArtifactoryPath(url, auth=(user, token)).exists()):
        print("Pulling {file} from {url}".format(file=file, url=url))
        path = artifactory.ArtifactoryPath(url, auth=(user, token))
        with path.open() as fd:
            with open(file, "wb") as out:
                out.write(fd.read())
    else:
        print("Artifact Not Found: {url}".format(url=url))

class Artifact(SkeleYaml):
    """
    Artifact Class

    Object contained within a list of the artifactory configuration in order to specify the
    artifact files and artifact names
    """

    schema = Schema({
        'name': And(str, error='Artifact \'name\' must be a String'),
        'file': And(str, error='Artifact \'file\' must be a String'),
    }, ignore_extra_keys=True)

    name = None
    file = None

    def __init__(self, name, file):
        self.name = name
        self.file = file

class Artifactory(Component):
    """
    Artifactory Component Class

    Provides the ability to push and pull artifacts that are defined in the skelebot config
    file to and from Artifactory based on the project version number
    """

    activation = Activation.CONFIG
    commands = ["push", "pull"]

    schema = Schema({
        Optional('artifacts'): And(list, error='Artifactory \'artifacts\' must be a List'),
        'url': And(str, error='Artifactory \'url\' must be a String'),
        'repo': And(str, error='Artifactory \'repo\' must be a String'),
        'path': And(str, error='Artifactory \'path\' must be a String'),
    }, ignore_extra_keys=True)

    artifacts = None
    url = None
    repo = None
    path = None

    @classmethod
    def load(cls, config):
        """Instantiate the Artifact Class Object based on a config dict"""

        cls.validate(config)

        artifactDicts = config["artifacts"]
        artifacts = []
        for artifact in artifactDicts:
            newArtifact = Artifact.load(artifact)
            artifacts.append(newArtifact)

        return cls(artifacts, config["url"], config["repo"], config["path"])

    def __init__(self, artifacts=None, url=None, repo=None, path=None):
        """Instantiate the Artifact Class Object based on the provided parameters"""

        self.artifacts = artifacts if artifacts is not None else []
        self.url = url
        self.repo = repo
        self.path = path

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
        parser.add_argument("-u", "--user", help="Auth user for Artifactory")
        parser.add_argument("-t", "--token", help="Auth token for Artifactory")
        parser.add_argument("-f", "--force", action='store_true', help="Force the push")

        parser = subparsers.add_parser("pull", help="Pull an artifact from artifactory")
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("version", help="The version of the artifact to pull")
        parser.add_argument("-u", "--user", help="Auth user for Artifactory")
        parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        return subparsers

    def execute(self, config, args):
        """
        Execution Hook

        Executes either the push or pull command depending on which one was provided to push
        rename the artifact and push it to Artifactory or pull down the given artifact version
        from Artifactory
        """

        artifactory.global_config = {
            self.url: {
                'username': None,
                'verify': True,
                'cert': None,
                'password': None
            }
        }

        # Get User and Token if not provided in args
        user = args.user
        token = args.token
        if (user is None):
            user = input("Please provide a valid Artifactory user: ")

        if (token is None):
            token = input("Please provide a valid Artifactory token: ")

        # Obtain the artifact that matches the provided name
        selectedArtifact = None
        for artifact in self.artifacts:
            if (artifact.name == args.artifact):
                selectedArtifact = artifact

        # Generate the local artifact file and the final Artifactory url path
        ext = selectedArtifact.file.split(".")[1]
        version = config.version if (args.job == "push") else args.version
        file = "{filename}_v{version}.{ext}"
        file = file.format(filename=selectedArtifact.name, version=version, ext=ext)
        url = "{url}/{repo}/{path}/{file}"
        url = url.format(url=self.url, repo=self.repo, path=self.path, file=file)

        # Push the artifact with the config version, or pull with the arg version
        if (args.job == "push"):
            pushArtifact(selectedArtifact.file, user, token, file, url, args.force)
        elif (args.job == "pull"):
            pullArtifact(user, token, file, url)
