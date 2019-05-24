from ..objects.component import *
from ..systems.execution import docker
from ..systems.generators import dockerfile, dockerignore

# This component provides the ability to spin up Jupyter in Docker for any project
class Prime(Component):
    activation = Activation.PROJECT
    commands = ["prime"]

    # Parser for the command that primes the docker image for deployment or subsequent job execution
    def addParsers(self, subparsers):
        helpMessage = "Generate Dockerfile and .dockerignore and build the docker image"
        parser = subparsers.add_parser("prime", help=helpMessage)
        return subparsers

    # Generate the Dockerfile and dockerignore and build the docker image
    def execute(self, config, args):

        return docker.build(config)
