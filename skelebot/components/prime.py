"""Prime Component"""

from ..objects.component import Activation, Component
from ..systems.execution import docker

class Prime(Component):
    """
    Prime Class

    This component provides the ability to prime a skelebot build by constructing the Dockerfile,
    the .dockerignore file, and building the docker image for the project
    """

    activation = Activation.PROJECT
    commands = ["prime"]

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the prime command that primes the docker image for deployment or
        subsequent job execution
        """

        helpMessage = "Generate Dockerfile and .dockerignore and build the docker image"
        primeParser = subparsers.add_parser("prime", help=helpMessage)
        primeParser.add_argument("-o", "--output", help="Output file name for the image file")
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        When the prime command is provided the Dockerfile, dockerignore file, and docker image are
        built so as to be ready for deployment
        """

        status = docker.build(config, host=host, verbose=args.verbose_global)
        if (status == 0) & (args.output is not None):
            status = docker.save(config, args.output, host=host, verbose=args.verbose_global)

        if (status > 0):
            raise Exception("Priming Failed")
