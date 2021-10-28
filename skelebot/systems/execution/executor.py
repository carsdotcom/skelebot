"""Execution System"""

import sys
from subprocess import call
from ...common import VERSION
from ..scaffolding.scaffolder import scaffold
from .commandBuilder import build as buildCommand
from .docker import build as buildDocker
from .docker import run as runDocker
from ...common import INFO

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
    host = config.getHost(job=job, args=args)

    is_native = args.native_global
    if (job.native == "always"):
        is_native = True
    elif (job.native == "never"):
        is_native = False

    if (is_native):
        if args.verbose_global:
            print(INFO.format(command))
        status = call(command, shell=True)
    else:
        if (not args.skip_build_global):
            buildDocker(config, host=host, verbose=args.verbose_global)
        ports = sorted(list(set(config.ports + job.ports)))
        status = runDocker(
            config, command, job.mode, ports, job.mappings, job.name, host=host,
            verbose=args.verbose_global
        )
    return(status)

def executeComponent(config, args):
    """Execute a Component of Skelebot"""
    host = config.getHost(args=args)

    for component in config.components:
        if (args.job in component.commands):
            component.execute(config, args, host=host)
