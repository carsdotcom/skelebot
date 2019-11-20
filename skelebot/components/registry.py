"""Registry Component"""

from schema import Schema, And, Optional
from ..objects.component import Activation, Component
from ..systems.execution import docker

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
    }, ignore_extra_keys=True)

    host = None
    port = None
    user = None

    def __init__(self, host=None, port=None, user=None):
        """Instantiate the Registry Class Object based on the provided parameters"""
        self.host = host
        self.port = port
        self.user = user

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

    def execute(self, config, args):
        """
        Execution Hook

        Executes when the publish command is provided and prompts for username and password before
        building the project's Docker Image and pushing it to the defined registry.
        """

        docker.login(self.host)
        docker.build(config)
        docker.push(config, self.host, self.port, self.user, tags=args.tags)
