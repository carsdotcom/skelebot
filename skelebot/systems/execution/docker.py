"""Docker Execution"""

import os
from subprocess import call
from ...systems.generators import dockerfile
from ...systems.generators import dockerignore

AWS_LOGIN_CMD = "$(aws ecr get-login --no-include-email --region {region} --profile {profile})"
AWS_LOGIN_CMD_V2 = "aws ecr get-login-password | docker login --username AWS --password-stdin {}"
LOGIN_CMD = "docker login {}"
BUILD_CMD = "docker build -t {image} ."
RUN_CMD = "docker run --name {image}-{jobName} --rm {params} {image} /bin/bash -c \"{command}\""
RUN_ENTRY_CMD = "docker run --name {image}-{jobName} --rm {params} --entrypoint {command} {image} {parameters}"
SAVE_CMD = "docker save -o {filename} {image}"
TAG_CMD = "docker tag {src} {image}:{tag}"
PUSH_CMD = "docker push {image}:{tag}"

def execute(cmd, err_msg="Docker Command Failed"):
    status = call(cmd, shell=True)
    if (status != 0):
        raise Exception(err_msg)

    return status

def login(host=None):
    """Login to the given Docker Host"""

    host = host if host is not None else ""
    loginCMD = LOGIN_CMD.format(host)

    print(loginCMD)
    status = execute(loginCMD, err_msg="Docker Login Failed")

    return status

def loginAWS(host=None, region=None, profile=None):
    """Login to AWS with ~/.aws credentials to access an ECR host"""

    host = host if host is not None else ""
    region = region if region is not None else "us-east-1"
    profile = profile if profile is not None else "default"

    try:
        loginCMD = AWS_LOGIN_CMD_V2.format(host)

        print(loginCMD)
        status = execute(loginCMD, err_msg="Docker Login V2 Failed")
    # If AWS CLI V2 authentication failed try V1 command...
    except Exception:
        loginCMD = AWS_LOGIN_CMD.format(region=region, profile=profile)

        print(loginCMD)
        status = execute(loginCMD, err_msg="Docker Login V1 Failed")

    return status

def build(config):
    """Build the Docker Image after building the Dockerfile and .dockerignore from Config"""

    # Build Dockerfile, .dockerignore, and Docker Image
    dockerfile.buildDockerfile(config)
    dockerignore.buildDockerignore(config)

    buildCMD = BUILD_CMD.format(image=config.getImageName())

    try:
        status = execute(buildCMD, err_msg="Docker Build Failed")
    finally:
        # Remove Files if ephemeral is set to True in Config
        if (config.ephemeral):
            os.remove("Dockerfile")
            os.remove(".dockerignore")

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
    if config.primaryExe == "CMD":
        runCMD = RUN_CMD.format(image=image, jobName=task, command=command, params=params, mode=mode)
    elif config.primaryExe == "ENTRYPOINT":
        commandParts = command.split(" ")
        extCommand = commandParts.pop(0)
        parameters = " ".join(commandParts)
        runCMD = RUN_ENTRY_CMD.format(image=image, jobName=task, command=extCommand, params=params, mode=mode, parameters=parameters)
    return execute(runCMD)

def save(config, filename="image.img"):
    """Save the Image File to the disk"""

    return execute(SAVE_CMD.format(image=config.getImageName(), filename=filename))

def push(config, host=None, port=None, user=None, tags=None):
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
        status = execute(TAG_CMD.format(src=imageName, image=image, tag=tag))
        status = execute(PUSH_CMD.format(image=image, tag=tag))

    return status
