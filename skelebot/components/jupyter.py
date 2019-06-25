from ..objects.component import *
from ..systems.execution import docker

# This component provides the ability to spin up Jupyter in Docker for any project
class Jupyter(Component):
    activation = Activation.PROJECT
    commands = ["jupyter"]

    port = None
    folder = None

    # Allows for intelligent defaults in the constructor so projects without config can still use the component
    def __init__(self, port=8888, folder="."):
        self.port = port
        self.folder = folder

    # Parser for the command that spins up Jupyter inside the Docker Container based on the given port and folder
    def addParsers(self, subparsers):
        helpMessage = "Spin up Jupyter in a Docker Container (port = {port}, folder = {folder})".format(port=self.port, folder=self.folder)
        parser = subparsers.add_parser("jupyter", help=helpMessage)
        return subparsers

    # Build the docker image and then run the container with the Jupyter command, port mapped, and folder volume mapped
    def execute(self, config, args):

        docker.build(config)

        command = "jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir={folder}".format(folder=self.folder)
        ports = ["{port}:8888".format(port=self.port)]

        print("Notebook Starting on localhost:{port}".format(port=self.port))
        print("Copy the token below to authenticate with Jupyter")

        return docker.run(config, command, "i", ports, ".", "jupyter")
