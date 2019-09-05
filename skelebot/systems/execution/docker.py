"""Docker Execution"""

import os
from ...systems.generators import dockerfile
from ...systems.generators import dockerignore

BUILD_CMD = "docker build -t {image} ."
RUN_CMD = "docker run --name {image}-{jobName} --rm {params} {image} /bin/bash -c \"{command}\""
SAVE_CMD = "docker save -o {filename} {image}"

def build(config):
    """Build the Docker Image after building the Dockerfile and .dockerignore from Config"""

    # Build Dockerfile, .dockerignore, and Docker Image
    dockerfile.buildDockerfile(config)
    dockerignore.buildDockerignore(config)
    status = os.system(BUILD_CMD.format(image=config.getImageName()))

    # Remove Files if ephemeral is set to True in Config
    if (config.ephemeral):
        os.remove("Dockerfile")
        os.remove(".dockerignore")

    # Raise an error if the build process failed
    if (status > 0):
        raise Exception("Docker Build Failed")

    return status

def run(config, command, mode, ports, mappings, task):
    """Run the Docker Container from the Image with the provided command"""

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
                params += " -v {pwd}/{vmap}:/app/{vmap}".format(pwd=os.getcwd(), vmap=vmap)

    # Construct the additional parameters from the components
    for component in config.components:
        addParams = component.addDockerRunParams()
        if (addParams is not None):
            params += " {params}".format(params=addParams)

    # Assuming the image was built without errors, run the container with the given command
    image = config.getImageName()
    runCMD = RUN_CMD.format(image=image, jobName=task, command=command, params=params, mode=mode)
    return os.system(runCMD)

def save(config, filename="image.img"):
    return os.system(SAVE_CMD.format(image=config.getImageName(), filename=filename))
