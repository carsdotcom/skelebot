"""Registry Component"""

from schema import Schema, And, Optional
from ..objects.skeleYaml import SkeleYaml
from ..objects.component import Activation, Component
from ..systems.execution import docker

class Aws(SkeleYaml):
    """
    AWS Specific Registry Details

    Provides the fields necessary for authenticating with an AWS ECR: region and profile.
    """

    schema = Schema({
        'region': And(str, error='Registry AWS \'region\' must be a String'),
        Optional('profile'): And(str, error='Registry AWS \'profile\' must be a String')
    }, ignore_extra_keys=True)

    region = None
    profile = None

    def __init__(self, region=None, profile=None):
        """Instantiate the Registry Class Object based on the provided parameters"""
        self.region = region
        self.profile = profile

class Registry(Component):
    """
    Registry Class

    Provides the ability to define the registry that will be used when publishing the Docker image
    for the project, and provides the capability to publish by logging into the registry through
    the CLI.
    """

    activation = Activation.PROJECT
    commands = ["publish"]

    schema = Schema({
        Optional('host'): And(str, error='Registry \'host\' must be a String'),
        Optional('port'): And(int, error='Registry \'port\' must be an Integer'),
        Optional('user'): And(str, error='Registry \'user\' must be a String'),
        Optional('aws'): And(dict, error='Registry \'aws\' must be a Dictionary')
    }, ignore_extra_keys=True)

    host = None
    port = None
    user = None
    aws = None

    @classmethod
    def load(cls, config):
        """Instantiate the AWS Class Object if it is present"""

        cls.validate(config)
        aws = Aws.load(config["aws"]) if ("aws" in config) else None

        return cls(config.get("host"), config.get("port"), config.get("user"), aws)

    def __init__(self, host=None, port=None, user=None, aws=None):
        """Instantiate the Registry Class Object based on the provided parameters"""
        self.host = host
        self.port = port
        self.user = user
        self.aws = aws

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the publish command to allow the user to login and push the project's
        Docker image to the defined registry, or Docker Hub, if one is not defined.
        """

        helpMessage = "Publish your versioned Docker Image to the registry"
        registryParser = subparsers.add_parser("publish", help=helpMessage)
        registryParser.add_argument("-t", "--tags", nargs='*', help="Additional image tags")

        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executes when the publish command is provided and prompts for username and password before
        building the project's Docker Image and pushing it to the defined registry.
        """

        # Login to the registry
        if self.aws is not None:
            docker.loginAWS(
                self.host, self.aws.region, self.aws.profile, docker_host=host,
                verbose=args.verbose_global
            )
        else:
            docker.login(host=self.host, docker_host=host, verbose=args.verbose_global)

        # Build and Push with the different tags (LATEST and VERSION default)
        if (not args.skip_build_global):
            docker.build(config, host=host, verbose=args.verbose_global)

        docker.push(
            config, self.host, self.port, self.user, tags=args.tags,
            docker_host=host, verbose=args.verbose_global
        )
