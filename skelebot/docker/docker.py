from ..objects.config import Config
from ..files.dockerfile import buildDockerfile
from ..files.dockerignore import buildDockerignore

import os

BUILD_CMD = "docker build -t {image} ."
RUN_CMD = "docker run --name {image}-{jobName} --rm {params} {image} /bin/bash -c '{command}'"

def build(config):
    buildDockerfile(config)
    buildDockerignore(config)

    status = os.system(BUILD_CMD.format(image=config.getImageName()))
    if (config.ephemeral == True):
        os.remove("Dockerfile")
        os.remove(".dockerignore")

    return status

def run(config, job, command):
    # [TODO] Kerberos Component - Construct the kerberos volume mappings and init command if required
    #krbInit = ""
    #if (config.kerberos != None):
        #krbInit = "/./krb/init.sh {user} &&".format(user=config.kerberos.hdfsUser)

    params = "-{mode}".format(mode=job.mode)
    
    # Construct the port mappings
    if (config.ports):
        for port in config.params:
            params += " -p {port}".format(port=port)

    # Construct the volume mappings
    if (job.mappings):
        for vmap in job.mappings:
            params += " -v $PWD/{vmap}:/app/{vmap}".format(vmap=vmap)

    # Construct the additional parameters from the components
    for component in config.components:
        addParams = component.addDockerRunParams(job)
        if (addParams is not None):
            params += " {params}".format(params=addParams)

    # Assuming the image was built without errors, run the container with the given args, params, and config
    return os.system(RUN_CMD.format(image=config.getImageName(), jobName=job.name, command=command, params=params, mode=job.mode))
