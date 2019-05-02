import os
import sys
from artifactory import ArtifactoryPath

def pushArtifact(artifact, version, user=None, token=None, force=False):

    dpl = artifact.deploy
    file = "{filename}_v{version}.{ext}".format(filename=artifact.name, version=version, ext=artifact.file.split(".")[1])
    url = "{url}/{repo}/{path}/{file}".format(url=dpl.url, repo=dpl.repo, path=dpl.path, file=file)

    if (force == False and ArtifactoryPath("{url}".format(url=url)).exists()):
        print("This artifact version has already been pushed. Please bump the version before pushing (skelebot bump) or force push (-f).")
        sys.exit(1)

    if (user == None):
        user = input("Please provide a valid Artifactory user: ")

    if (token == None):
        token = input("Please provide a valid Artifactory token: ")

    print("Deploying {file} to {url}".format(file=file, url=url))
    path = ArtifactoryPath(url, auth=(user, token))
    os.rename(artifact.file, file)
    try:
        path.deploy_file(file)
    except:
        os.rename(file, artifact.file)
        raise
    os.rename(file, artifact.file)

def pullArtifact(artifact, version, user=None, token=None):

    dpl = artifact.deploy
    file = "{filename}_v{version}.{ext}".format(filename=artifact.name, version=version, ext=artifact.file.split(".")[1])
    url = "{url}/{repo}/{path}/{file}".format(url=dpl.url, repo=dpl.repo, path=dpl.path, file=file)

    if (ArtifactoryPath("{url}".format(url=url)).exists()):

        if (user == None):
            user = input("Please provide a valid Artifactory user: ")

        if (token == None):
            token = input("Please provide a valid Artifactory token: ")

        print("Pulling {file} from {url}".format(file=file, url=url))
        path = ArtifactoryPath(url, auth=(user, token))
        with path.open() as fd:
            with open(file, "wb") as out:
                    out.write(fd.read())
    else:
        print("Artifact Not Found: {url}".format(url=url))
