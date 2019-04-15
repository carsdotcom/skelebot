import os
from .dname import getImageName
from .docker import buildDockerfile
from .dockerignore import buildDockerignore

def dbuild(config, runJob=None, skipBuild=False):
    config.generateFile(buildDockerfile(config), "Dockerfile")
    config.generateFile(buildDockerignore(config, runJob), ".dockerignore")

    status = 0
    if (skipBuild == False):
        name = getImageName(config)
        status = status + os.system("docker build -t " + name + " .")
        if (config.ephemeral == True):
            os.remove("Dockerfile")
    return status
