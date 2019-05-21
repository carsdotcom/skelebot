from ..objects.component import *
from ..systems.execution import docker
from ..systems.generators import dockerfile, dockerignore

# This component provides a way to spin up the container and exec into it for debugging or testing
class Dexec(Component):
    activation = Activation.PROJECT
    commands = ["exec"]

    # Parser for the command that exec into the docker container
    def addParsers(self, subparsers):
        helpMessage = "Exec into the running Docker container"
        parser = subparsers.add_parser("exec", help=helpMessage)
        return subparsers

    # Generate the Dockerfile and dockerignore and build the docker image and exec into the container
    def execute(self, config, args):

        docker.build(config)
        docker.run(config, "/bin/bash", "it", [], [], "{}-exec".format(config.getImageName()))
