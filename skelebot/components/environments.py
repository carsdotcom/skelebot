"""Environments Component"""

import os
import re
from schema import Schema, And, Optional
from ..objects.component import Activation, Component
from ..systems.execution import docker

HELP_MESSAGE = "Display the available environments for the project"

class Environments(Component):
    """
    Envs Class

    Provides the ability to inspect the available environments for the project.
    """

    activation = Activation.PROJECT
    commands = ["envs"]

    def addParsers(self, subparsers):
        """
        SkeleParser Hook

        Adds a parser for the envs command to list the available skelebot environments. 
        """

        subparsers.add_parser("envs", help=HELP_MESSAGE)
        return subparsers

    def execute(self, config, args, host=None):
        """
        Execution Hook

        Executed when the envs command is provided it reads the skelebot files from the local
        project to determine the list of available environments.
        """

        envs = ["[default]"]

        # Read envs from disk
        for fl in os.listdir():
            if re.match("skelebot-\\w+[.]yaml", fl):
                fl = fl.split("-")[1]
                fl = fl.split(".")[0]
                envs.append(fl)

        # Print the list of envs
        for env in envs:
            print(env)

        return 0
