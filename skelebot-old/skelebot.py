from .scaffold import scaffold
from .execute import execute
from .semver.version import bumpVersion
from .config.config import Config
from .config.yaml import override
from .artifactory.artifactory import pushArtifact, pullArtifact
from .plugin.plugin import installPlugin, pluginCommand
from .docker.djupyter import jupyter
from .globals import VERSION
from .docker.dexec import dexec
from .docker.dbuild import dbuild
import os
import sys
import yaml
import argparse
from argparse import RawTextHelpFormatter

# The main method for the skelebot CLI project management tool
def main():
    # Obtain the env manually from the args
    isNext = False
    env = None
    for arg in sys.argv:
        if (isNext):
            env = arg
            isNext = False
        if (arg == "-e") or (arg == "--env"):
            isNext = True

    # Read the skelebot config file if it is present
    cwd = os.getcwd()
    config = None
    pName = None
    pDesc = None
    pVersion = None
    cfgFile = "{path}/skelebot.yaml".format(path=cwd)
    if os.path.isfile(cfgFile):
        with open(cfgFile, 'r') as stream:
            cfg = yaml.load(stream)
            if (env):
                # Read the env specific details if an env parameter was passed
                envFile = "{path}/skelebot-{env}.yaml".format(path=cwd, env=env)
                if os.path.isfile(envFile):
                    with open(envFile, 'r') as stream:
                        cfgOverride = yaml.load(stream)
                        cfg = override(cfg, cfgOverride)

            config = Config.load(cfg)
            pName = " ".join([word.capitalize() for word in config.name.split("-")])
            pDesc = config.description
            pVersion = config.version
            pSkeleVersion = config.skelebotVersion

    # Create the arg parser and subparsers
    desc = "Skelebot Version: {version}".format(version=VERSION)
    if (config != None):
        desc = """
\033[1m{project}\033[0m
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version (project): {sbVersion}
Skelebot Version (installed): {version}
-----------------------------------"""
        desc = desc.format(sbVersion=pSkeleVersion, version=VERSION, project=pName, desc=pDesc, pVersion=pVersion, env=env)
    parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="job")


    # Add the plugin command for installing new skelebot plugins from zip files
    pluginParser = subparsers.add_parser("plugin", help="Install a plugin for skelebot from a local zip file")
    pluginParser.add_argument("plugin", help="The zip file of the skelebot plugin")

    if (config == None):
        # Add scaffolding job since this is not a skelebot project
        subparser = subparsers.add_parser("scaffold", help="Scaffold a new skelebot project from scratch")
        subparser.add_argument("-e", "--existing", action="store_true", help="Setup the skelebot.yaml for an existing project")
    if (config != None):
        # Add global command arguments
        parser.add_argument("-e", "--env", help="Specify the runtime environment configurations")
        parser.add_argument("-s", "--skip-build", action='store_true', help="Skip the build process and attempt to use previous docker build")
        parser.add_argument("-n", "--native", action='store_true', help="Run natively instead of through Docker")

        # Add the bump version task now that it's a skelebot project
        versionParser = subparsers.add_parser("bump", help="Increment the version of the project")
        versionParser.add_argument("mmp", choices=["major", "minor", "patch"])

        # Add the prime task to generate needed project files
        primeParser = subparsers.add_parser("prime", help="Prime skelebot with latest config")
        primeParser.add_argument("-s", "--skip-build", action='store_true', help="Skip the build process during priming")

        # Add the exec task to allow easy access to the docker container
        execParser = subparsers.add_parser("exec", help="Start the Docker container and access it via bash")

        # Add the exec task to allow easy access to the docker container
        jpyParser = subparsers.add_parser("jupyter", help="Start a Jupyter notebook inside of Docker")

        # Add the push artifactory job - should be a plugin
        if (config.artifacts != None):
            artifactParser = subparsers.add_parser("push", help="Push an artifact to artifactory")
            artifactParser.add_argument("-u", "--user", help="Auth user for Artifactory")
            artifactParser.add_argument("-t", "--token", help="Auth token for Artifactory")
            artifactParser.add_argument("-f", "--force", action='store_true', help="Force the artifact to be pushed")
            # Add artifacts from config to the list of choices
            artifactNames = []
            for artifact in config.artifacts:
                artifactNames.append(artifact.name)

            artifactParser.add_argument("artifact", choices=artifactNames)

            artifactParser = subparsers.add_parser("pull", help="Pull an artifact from artifactory")
            artifactParser.add_argument("artifact", choices=artifactNames)
            artifactParser.add_argument("version", help="The version of the artifact to pull")
            artifactParser.add_argument("-u", "--user", help="Auth user for Artifactory")
            artifactParser.add_argument("-t", "--token", help="Auth token for Artifactory")

        # Add the plugin commands to the parser and construct a list of the plugin names
        plugins = []
        if (config.plugins != None):
            for plugin in config.plugins:
                subparsers.add_parser(plugin.name, help="Command for the {plugin} plugin".format(plugin=plugin.name))
                plugins.append(plugin.name)
                

        # Add jobs from config to the subparser
        if (config.jobs != None):
            for job in config.jobs:
                subparser = subparsers.add_parser(job.name, help=job.help + " (" + job.source + ")")

                # Add args to the job if they are present in the config
                if (job.args != None):
                    for arg in job.args:
                        if (arg.choices != None):
                            subparser.add_argument(arg.name, choices=arg.choices)
                        else:
                            subparser.add_argument(arg.name)

                # Add params to the job if they are present in the config
                if (job.params != None):
                    for param in job.params:
                        if (param.choices != None):
                            subparser.add_argument("-" + param.alt, "--" + param.name, choices=param.choices)
                        else:
                            subparser.add_argument("-" + param.alt, "--" + param.name)

    # Parse the args
    args = parser.parse_args()

    # Execute the job or start scaffolding (print help if no command provided)
    if (args.job == None):
        parser.print_help()
    elif (args.job == "plugin"):
        installPlugin(args.plugin)
    elif (args.job == "scaffold"):
        scaffold(cwd, args.existing)
    elif (args.job == "prime"):
        dbuild(config, skipBuild=args.skip_build)
    elif (args.job == "exec"):
        dexec(config)
    elif (args.job == "push"):
        artifact = None
        for art in config.artifacts:
            if (args.artifact == art.name):
                artifact = art
        pushArtifact(artifact, config.version, args.user, args.token, args.force)
    elif (args.job == "pull"):
        artifact = None
        for art in config.artifacts:
            if (args.artifact == art.name):
                artifact = art
        pullArtifact(artifact, args.version, args.user, args.token)
    elif (args.job == "bump"):
        config = bumpVersion(config, args.mmp)
        config.generateYaml()
    elif (args.job in plugins):
        pluginCommand(config, args.job)
    elif (args.job == "jupyter"):
        jupyter(config, args)
    else:
        execute(config, args)

