from ..scaffolding.scaffolder import scaffold
from .commandBuilder import build as buildCommand
from .docker import build as buildDocker
from .docker import run as runDocker
import argparse
import os

def execute(config, sbParser):
    args = sbParser.parseArgs()

    if (args.job == None):
        sbParser.showHelp()
    elif (args.job == "scaffold"):
        scaffold(args.existing)
    else:
        job = getJob(config, args)

        if (job is not None):
            executeJob(config, args, job)
        else:
            executeComponent(config, args)

def getJob(config, args):
    job = None
    for configJob in config.jobs:
        if args.job == configJob.name:
            job = configJob

    return job

def executeJob(config, args, job):
        command = buildCommand(config, job, args, args.native)
        if (args.native):
            os.system(command)
        else:
            if (args.skip_build == False):
                buildDocker(config)
            runDocker(config, command, job.mode, config.ports, job.mappings, job.name)

def executeComponent(config, args):
    for component in config.components:
        if (args.job in component.commands):
            component.execute(config, args)
