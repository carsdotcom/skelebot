from ..objects.component import *
from ..objects.skeleYaml import SkeleYaml

import shutil
import artifactory
import os

ERROR_ALREADY_PUSHED = """This artifact version has already been pushed.
Please bump the version before pushing (skelebot bump) or force push (-f)."""

class Artifact(SkeleYaml):
    name = None
    file = None

    def __init__(self, name, file):
        self.name = name
        self.file = file

# This component provides the ability to spin up Jupyter in Docker for any project
class Artifactory(Component):
    activation = Activation.CONFIG
    commands = ["push", "pull"]

    artifacts = None
    url = None
    repo = None
    path = None

    # Load the yaml dict structure into the Artifactory class object and child object list
    @classmethod
    def load(cls, config):
        artifactDicts = config["artifacts"]
        artifacts = []
        for artifact in artifactDicts:
            newArtifact = Artifact(artifact["name"], artifact["file"])
            artifacts.append(newArtifact)
        return cls(artifacts, config["url"], config["repo"], config["path"])

    def __init__(self, artifacts=[], url=None, repo=None, path=None):
        self.artifacts = artifacts
        self.url = url
        self.repo = repo
        self.path = path

    # Parser for the push and pull commands to push and pull artifacts to/from Artifactory
    def addParsers(self, subparsers):
        artifactNames = []
        for artifact in self.artifacts:
            artifactNames.append(artifact.name)

        parser = subparsers.add_parser("push", help="Push an artifact to artifactory")
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("-u", "--user", help="Auth user for Artifactory")
        parser.add_argument("-t", "--token", help="Auth token for Artifactory")
        parser.add_argument("-f", "--force", action='store_true', help="Force the artifact to be pushed")

        parser = subparsers.add_parser("pull", help="Pull an artifact from artifactory")
        parser.add_argument("artifact", choices=artifactNames)
        parser.add_argument("version", help="The version of the artifact to pull")
        parser.add_argument("-u", "--user", help="Auth user for Artifactory")
        parser.add_argument("-t", "--token", help="Auth token for Artifactory")

        return subparsers

    # Generate the Dockerfile and dockerignore and build the docker image
    def execute(self, config, args):
        # Get User and Token if not provided in args
        user = None
        token = None
        if (args.user == None):
            user = input("Please provide a valid Artifactory user: ")

        if (args.token == None):
            token = input("Please provide a valid Artifactory token: ")

        # Obtain the artifact that matches the provided name
        selectedArtifact = None
        for artifact in self.artifacts:
            if (artifact.name == args.artifact):
                selectedArtifact = artifact

        # Generate the local artifact file and the final Artifactory url path
        ext = selectedArtifact.file.split(".")[1]
        version = config.version if (args.job == "push") else args.version
        file = "{filename}_v{version}.{ext}".format(filename=selectedArtifact.name, version=version, ext=ext)
        url = "{url}/{repo}/{path}/{file}".format(url=self.url, repo=self.repo, path=self.path, file=file)

        # Push the artifact with the config version, or pull with the arg version
        if (args.job == "push"):
            self.pushArtifact(selectedArtifact.file, user, token, file, url, args.force)
        elif (args.job == "pull"):
            self.pullArtifact(user, token, file, url)

    def pushArtifact(self, artifactFile, user, token, file, url, force):

        # Error and exit if artifact already exists and we are not forcing an override
        if (force == False) and artifactory.ArtifactoryPath(url).exists():
            raise Exception(ERROR_ALREADY_PUSHED)

        # Rename artifact, deploy the renamed artifact, and then rename it back to original name
        print("Deploying {file} to {url}".format(file=file, url=url))
        path = artifactory.ArtifactoryPath(url, auth=(user, token))
        shutil.copyfile(artifactFile, file)
        try:
            path.deploy_file(file)
        except:
            raise
        finally:
            os.remove(file)

    def pullArtifact(self, user, token, file, url):

        # Pull the artifact with the given url and save it to the file path
        if (artifactory.ArtifactoryPath(url).exists()):
            print("Pulling {file} from {url}".format(file=file, url=url))
            path = artifactory.ArtifactoryPath(url, auth=(user, token))
            with path.open() as fd:
                with open(file, "wb") as out:
                    content = fd.read()
                    print(content)
                    out.write(fd.read())
        else:
            print("Artifact Not Found: {url}".format(url=url))
