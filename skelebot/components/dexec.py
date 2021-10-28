"""Docker Exec Component"""

from ..objects.component import Activation, Component
from ..systems.execution import docker

class Dexec(Component):
    """
    Docker Exec Class

    Provides a command to access the project container via bash prompt with the option volume map
    the contents of the project into the container so that they can be modified as root
    """

    activation = Activation.PROJECT
    commands = ["exec"]

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the exec command that allows for bash access to the project container
        along with full project volume mapping support via an optional parameter flag
        """

        helpMessage = "Exec into the running Docker container"
        argHelp = "Volume map the working directory onto the container"
        parser = subparsers.add_parser("exec", help=helpMessage)
        parser.add_argument("-m", "--map", action="store_true", help=argHelp)
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executes when the exec command is provided and runs the container with the /bin/bash
        command in order to provide access to the user
        """

        mappings = []
        if (args.map):
            mappings.append(".")

        docker.build(config, host=host, verbose=args.verbose_global)
        docker.run(
            config, "/bin/bash", "it", [], mappings, "exec", host=host,
            verbose=args.verbose_global
        )
