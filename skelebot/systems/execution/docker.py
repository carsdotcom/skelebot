"""Docker Execution"""

import os
from subprocess import call
from .dockerCommand import DockerCommandBuilder
from ...systems.generators import dockerfile
from ...systems.generators import dockerignore
from ...common import INFO

AWS_LOGIN_CMD = "$(aws ecr get-login --no-include-email --region {region} --profile {profile})"
AWS_LOGIN_CMD_V2 = "aws ecr get-login-password --region {region} --profile {profile} | docker{docker_host} login --username AWS --password-stdin {host}"

def execute(cmd, err_msg="Docker Command Failed", verbose=False):
    if verbose:
        print(INFO.format(cmd))
    status = call(cmd, shell=True)
    if (status != 0):
        raise Exception(err_msg)

    return status

def login(host=None, docker_host=None, verbose=False):
    """Login to the given Docker Host"""

    host = host if host is not None else ""
    loginCMD = DockerCommandBuilder(host=docker_host).login(host)

    status = execute(loginCMD, err_msg="Docker Login Failed", verbose=verbose)

    return status

def loginAWS(host=None, region=None, profile=None, docker_host=None, verbose=False):
    """Login to AWS with ~/.aws credentials to access an ECR host"""

    host = host if host is not None else ""
    region = region if region is not None else "us-east-1"
    profile = profile if profile is not None else "default"

    try:
        v2_docker_host = " -H {}".format(docker_host) if docker_host is not None else  ""
        loginCMD = AWS_LOGIN_CMD_V2.format(
            region=region, profile=profile, docker_host=v2_docker_host, host=host
        )

        status = execute(loginCMD, err_msg="Docker Login V2 Failed", verbose=verbose)
    # If AWS CLI V2 authentication failed try V1 command...
    except Exception:
        if docker_host is not None:
            raise ValueError("Remote hosts are not supported by Docker Login V1")
        loginCMD = AWS_LOGIN_CMD.format(region=region, profile=profile)

        status = execute(loginCMD, err_msg="Docker Login V1 Failed", verbose=verbose)

    return status

def build(config, host=None, verbose=False):
    """Build the Docker Image after building the Dockerfile and .dockerignore from Config"""

    # Build Dockerfile, .dockerignore, and Docker Image
    dockerfile.buildDockerfile(config)
    dockerignore.buildDockerignore(config)

    buildCMD = DockerCommandBuilder(host=host).build(config.getImageName())

    try:
        status = execute(buildCMD, err_msg="Docker Build Failed", verbose=verbose)
    finally:
        # Remove Files if ephemeral is set to True in Config
        if (config.ephemeral):
            os.remove("Dockerfile")
            os.remove(".dockerignore")

    return status

def run(config, command, mode, ports, mappings, task, host=None, verbose=False):
    """Run the Docker Container from the Image with the provided command"""

    image = config.getImageName()
    run_name = "{image}-{job}".format(image=image, job=task)
    runCMD = DockerCommandBuilder(host=host).run(image).set_name(run_name).set_rm().set_mode(mode)

    if config.gpu:
        runCMD = runCMD.set_gpu()

    # Construct the port mappings
    if (ports):
        for port in ports:
            runCMD = runCMD.set_port(port)

    # Construct the volume mappings
    if (mappings):
        for vmap in mappings:
            if ("~" in vmap):
                vmap = vmap.replace("~", os.path.expanduser("~"))

            if (":" not in vmap):
                vmap = "{pwd}/{vmap}:/app/{vmap}".format(pwd=os.getcwd(), vmap=vmap)

            runCMD = runCMD.set_volume(vmap)

    # Construct the additional parameters from the components
    for component in config.components:
        addParams = component.addDockerRunParams()
        if (addParams is not None):
            runCMD = runCMD.set_params(addParams)

    # Assuming the image was built without errors, run the container with the given command
    if config.primaryExe == "ENTRYPOINT":
        commandParts = command.split(" ")
        command = commandParts.pop(0)
        parameters = " ".join(commandParts)
        runCMD = runCMD.set_entrypoint(parameters)

    return execute(runCMD.build(command), verbose=verbose)

def save(config, filename="image.img", host=None, verbose=False):
    """Save the Image File to the disk"""

    cmd = DockerCommandBuilder(host=host).save(config.getImageName()).set_output(filename).build()
    return execute(cmd, verbose=verbose)

def push(config, host=None, port=None, user=None, tags=None, docker_host=None, verbose=False):
    """Tag with version and latest and push the project Image to the provided Docker Image Host"""

    imageName = config.getImageName()
    port = ":{port}".format(port=port) if port is not None else ""
    host = "{host}{port}/".format(host=host, port=port) if host is not None else ""
    user = "{user}/".format(user=user) if user is not None else ""
    image = "{host}{user}{name}".format(host=host, user=user, name=imageName)

    tags = [] if tags is None else tags
    tags = tags + [config.version, "latest"]

    status = 0
    for tag in tags:
        status = execute(
            DockerCommandBuilder(host=docker_host).tag(imageName, image, tag),
            verbose=verbose
        )
        status = execute(
            DockerCommandBuilder(host=docker_host).push(image).set_tag(tag).build(),
            verbose=verbose
        )

    return status
