from ...objects.config import Config
from ...systems.generators import dockerfile
from ...systems.generators import dockerignore

import os

BUILD_CMD = "docker build -t {image} ."
RUN_CMD = "docker run --name {image}-{jobName} --rm {params} {image} /bin/bash -c '{command}'"

def build(config):
    dockerfile.buildDockerfile(config)
    dockerignore.buildDockerignore(config)

    status = os.system(BUILD_CMD.format(image=config.getImageName()))
    if (config.ephemeral == True):
        os.remove("Dockerfile")
        os.remove(".dockerignore")

    if (status > 0):
        raise Exception("Docker Build Failed")

    return status

def run(config, command, mode, ports, mappings, taskName):
    params = "-{mode}".format(mode=mode)

    # Construct the port mappings
    if (ports):
        for port in ports:
            params += " -p {port}".format(port=port)

    # Construct the volume mappings
    if (mappings):
        for vmap in mappings:
            if ("~" in vmap):
                vmap = vmap.replace("~", os.path.expanduser("~"))

            if (":" in vmap):
                params += " -v {vmap}".format(vmap=vmap)
            else:
                params += " -v $PWD/{vmap}:/app/{vmap}".format(vmap=vmap)

    # Construct the additional parameters from the components
    for component in config.components:
        addParams = component.addDockerRunParams()
        if (addParams is not None):
            params += " {params}".format(params=addParams)

    # Assuming the image was built without errors, run the container with the given args, params, and config
    return os.system(RUN_CMD.format(image=config.getImageName(), jobName=taskName, command=command, params=params, mode=mode))
