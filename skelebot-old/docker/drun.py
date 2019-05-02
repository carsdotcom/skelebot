import os
from .dbuild import dbuild
from .dname import getImageName
from .extensionCommands import extensionCommands

#TODO: This should be made more generic such that it can be leveraged by dexec and jupyter
def drun(config, runJob, arguments, params, skipBuild=False):
    # Construct the kerberos volume mappings and init command if required
    krbInit = ""
    if (config.kerberos != None):
        krbInit = "/./krb/init.sh {user} &&".format(user=config.kerberos.hdfsUser)

    # Construct the port mappings
    ports = ""
    if (config.ports):
        for port in config.ports:
            ports += " -p {port}".format(port=port)

    # Construct the volume mappings
    vmaps = ""
    if (runJob.mapped):
        for vmap in runJob.mapped:
            vmaps += " -v $PWD/{vmap}:/app/{vmap}".format(vmap=vmap)

    # Build the docker image if skipBuild not enabled
    status = dbuild(config, runJob, skipBuild)

    # Assuming the image was built without errors, run the container with the given args, params, and config
    if (status == 0):
        name = getImageName(config)
        ext = runJob.source.split(".")[1]
        runCMD = "docker run --name {image}-{jobName} --rm -{mode}{ports}{vmaps} {image} /bin/bash -c '{krbInit} {command}{script} {args} {params}'"
        runCMD = runCMD.format(jobName=runJob.name, image=name, krbInit=krbInit, command=extensionCommands[ext], vmaps=vmaps,
                           mode=runJob.mode, ports=ports, script=runJob.source, args=arguments, params=params)
        os.system(runCMD)
