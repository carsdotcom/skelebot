"""Jupyter Component"""

from schema import Schema, And, Optional
from ..objects.component import Activation, Component
from ..systems.execution import docker

HELP_TEMPLATE = "Spin up Jupyter in a Docker Container (port={port}, folder={folder})"
COMMAND_TEMPLATE = "jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir={folder}"

class Jupyter(Component):
    """
    Jupyter Class

    Provides the ability to spin up Jupyter notebooks inside a Docker container with the exact
    configuration as the rest of the project and it's jobs
    """

    activation = Activation.PROJECT
    commands = ["jupyter"]

    schema = Schema({
        Optional('port'): And(int, error='Jupyter \'port\' must be an Integer'),
        Optional('folder'): And(str, error='Jupyter \'folder\' must be a String'),
        Optional('mappings'): And(list, error='Jupyter \'mappings\' must be a List'),
    }, ignore_extra_keys=True)

    port = None
    folder = None
    mappings = None

    def __init__(self, port=8888, folder=".", mappings = '.'):
        """Initialize the class with simple default values for port and folder"""
        self.port = port
        self.folder = folder
        self.mappings = mappings

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the jupter command the starts up the notebooks in Docker
        """

        helpMessage = HELP_TEMPLATE.format(port=self.port, folder=self.folder)
        subparsers.add_parser("jupyter", help=helpMessage)
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executed when the jupyter command is provided it reads from the config to spin up a volume
        mapped container on the configured port with the configured folder based on the same image
        that the rest of the project utilizes
        """

        docker.build(config, host=host, verbose=args.verbose_global)

        command = COMMAND_TEMPLATE.format(folder=self.folder)
        ports = ["{port}:8888".format(port=self.port)]
        # Only map current dir if not running on remote host
        if host is None:
            mappings = ["."] + self.mappings if "." not in self.mappings else self.mappings
        else:
            mappings = self.mappings

        print("Notebook Starting on localhost:{port}".format(port=self.port))
        print("Copy the token below to authenticate with Jupyter")

        return docker.run(
            config, command, "it", ports, mappings, "jupyter", host=host,
            verbose=args.verbose_global
        )
