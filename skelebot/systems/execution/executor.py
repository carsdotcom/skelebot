"""Execution System"""

import os
import sys
from ...common import VERSION
from ..scaffolding.scaffolder import scaffold
from .commandBuilder import build as buildCommand
from .docker import build as buildDocker
from .docker import run as runDocker

def execute(config, sbParser, args=None):
    """Execute the command(s) that was sent into Skelebot based on the project Config"""

    args = args if args is not None else sys.argv[1:]
    for command in getCommands(args):
        args = sbParser.parseArgs(command)

        if (vars(args).get("version_global", False)):
            print("Skelebot v{}".format(VERSION))
        elif (vars(args).get("contact_global", False)):
            print(config.contact)
        elif (args.job is None):
            sbParser.showHelp()
        elif (args.job == "scaffold"):
            scaffold(args.existing)
        else:
            job = getJob(config, args)

            if (job is not None):
                status = executeJob(config, args, job)
                if status != 0:
                    sys.exit(status)
            else:
                executeComponent(config, args)

def getCommands(args):
    """Split (if needed) and obtain the list of commands that were sent into Skelebot"""

    commands = []
    command = []
    for arg in args:
        if arg == "+":
            commands.append(command)
            command = []
        else:
            command.append(arg)
    commands.append(command)

    return commands

def getJob(config, args):
    """Identify the job in the Config that matches the command that was sent to Skelebot"""

    job = None
    for configJob in config.jobs:
        if args.job == configJob.name:
            job = configJob

    return job

def executeJob(config, args, job):
    """Execute a Config job either natively or through Docker by building a command from it"""

    command = buildCommand(config, job, args, args.native_global)
    if (args.native_global):
        status = os.system(command)
    else:
        if (not args.skip_build_global):
            buildDocker(config)
        status = runDocker(config, command, job.mode, config.ports, job.mappings, job.name)
    return(status)

def executeComponent(config, args):
    """Execute a Component of Skelebot"""

    for component in config.components:
        if (args.job in component.commands):
            component.execute(config, args)
