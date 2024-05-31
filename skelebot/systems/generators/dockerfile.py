"""Dockerfile Generator"""

import os
import re
from subprocess import call
from ..execution import commandBuilder

try:
    import tomllib
except ModuleNotFoundError:
    # python <= 3.11
    import tomli as tomllib

FILE_PATH = "{path}/Dockerfile"

PY_DOWNLOAD_CA = "aws codeartifact get-package-version-asset --domain {domain} --domain-owner {owner} --repository {repo} --package {pkg} --package-version {version}{profile} --format pypi --asset {asset} libs/{asset}"
PY_INSTALL = 'RUN ["pip", "install", "{dep}"]\n'
PY_INSTALL_VERSION = 'RUN ["pip", "install", "{depName}=={version}"]\n'
PY_INSTALL_GITHUB = 'RUN ["pip", "install", "git+{depPath}"]\n'
PY_INSTALL_FILE = "COPY {depPath} {depPath}\n"
PY_INSTALL_FILE += 'RUN ["pip", "install", "/app/{depPath}"]\n'
PY_INSTALL_REQ = "COPY {depPath} {depPath}\n"
PY_INSTALL_REQ += 'RUN ["pip", "install", "-r", "/app/{depPath}"]\n'
TIMEZONE = "ENV TZ={timezone}\nRUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone\n"

DOCKERFILE = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

"""

def parse_pyproj(pyproject_file):
    """Parse all required and optional dependencies from pyproject file."""
    with open(os.path.join(os.getcwd(), pyproject_file), "rb") as f:
        pyproj = tomllib.load(f).get("project", {})

    deps = pyproj.get("dependencies", []).copy()
    for opt_deps in pyproj.get('optional-dependencies', {}).values():
        deps += opt_deps

    # Replace any double quotes in dependencies with single quotes so we don't
    # break the Dockerfile
    deps = [d.replace('"', "'") for d in deps]

    return '", "'.join(deps)


def buildDockerfile(config):
    """Generates the Dockerfile based on values from the Config object"""

    # Setup the basics of all dockerfiless
    docker = DOCKERFILE
    docker += "FROM {baseImage}\n".format(baseImage=config.getBaseImage())
    docker += "MAINTAINER {maintainer} <{contact}>\n".format(maintainer=config.maintainer, contact=config.contact)
    docker += "WORKDIR /app\n"

    if (config.timezone is not None):
        docker += TIMEZONE.format(timezone=config.timezone)

    # Add dependencies
    for dep in config.dependencies:
        depSplit = dep.split(":")
        if (dep.startswith("github:")):
            docker += PY_INSTALL_GITHUB.format(depPath=dep.split(":", maxsplit=1)[1])
        elif (dep.startswith("file:")):
            docker += PY_INSTALL_FILE.format(depPath=depSplit[1])
        elif (dep.startswith("req:")):
            docker += PY_INSTALL_REQ.format(depPath=depSplit[1])
        elif (dep.startswith("ca_file:")):
            domain = depSplit[1]
            owner = depSplit[2]
            repo = depSplit[3]
            pkg = depSplit[4]
            version = depSplit[5]
            asset = f"{pkg.replace('-', '_')}-{version}-py3-none-any.whl"
            profile = f" --profile {depSplit[6]}" if (len(depSplit) > 6) else ""
            cmd = PY_DOWNLOAD_CA.format(domain=domain, owner=owner, repo=repo, pkg=pkg, version=version, asset=asset, profile=profile)
            os.makedirs(os.path.join(os.getcwd(), 'libs'), exist_ok=True)
            status = call(cmd, shell=True)
            if (status != 0):
                raise Exception("Failed to Obtain CodeArtifact Package")

            docker += PY_INSTALL_FILE.format(depPath=f"libs/{asset}")
        elif (dep.startswith("proj:")):
            deps = parse_pyproj(depSplit[1])
            docker += PY_INSTALL.format(dep=deps)
        # if using PIP version specifiers, will be handled as a standard case
        elif dep.count("=") == 1 and not re.search(r"[!<>~]", dep):
            verSplit = dep.split("=")
            docker += PY_INSTALL_VERSION.format(depName=verSplit[0], version=verSplit[1])
        else:
            docker += PY_INSTALL.format(dep=dep)

    # Copy the project into the /app folder of the Docker Image
    # Ignores anything in the .dockerignore file of the project
    docker += "COPY . /app\n"

    # Run any custom global commands
    for command in config.commands:
        docker += "RUN {command}\n".format(command=command)

    # Pull in any additional dockerfile updates from the components
    for component in config.components:
        docker += component.appendDockerfile()

    # Set the CMD to execute the primary job by default (if there is one)
    for job in config.jobs:
        if config.primaryJob == job.name:

            if "CMD" == config.primaryExe:
                command = commandBuilder.build(config, job, None)
                docker += "CMD /bin/bash -c \"{command}\"\n".format(command=command)
            elif "ENTRYPOINT" == config.primaryExe:
                # ENTRYPOINT execution ignores any job and global arguments and parameters
                job_args = job.args
                job_params = job.params
                config_params = config.params
                job.args, job.params, config.params = [], [], []

                command = commandBuilder.build(config, job, None)
                commandParts = command.split(" ")
                docker += 'ENTRYPOINT ["{}"]\n'.format('", "'.join(commandParts))

                # Restore job and config for any downstream jobs
                job.args, job.params, config.params = job_args, job_params, config_params

            break

    with open(FILE_PATH.format(path=os.getcwd()), "w", encoding="utf-8") as dockerfile:
        dockerfile.write(docker)
