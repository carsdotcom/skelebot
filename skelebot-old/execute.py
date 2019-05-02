from .docker.drun import drun
from .docker.extensionCommands import extensionCommands
import os

def execute(config, args):
    # Identify the job to run
    runJob = None
    ext = None
    for job in config.jobs:
        if args.job == job.name:
            runJob = job
            ext = runJob.source.split(".")[1]

    # Construct the string of arguments
    arguments = ""
    if (runJob.args != None):
        for arg in runJob.args:
            value = vars(args)[arg.name]
            if (value == None):
                value = arg.default
            if (value != None):
                arguments = arguments + value + " "

    # Construct the string of parameters
    params = ""
    if (runJob.params != None):
        for param in runJob.params:
            value = vars(args)[param.name]
            if (value == None):
                value = param.default
            if (value != None):
                params = params + "--" + param.name + " " + value + " "

    # Execute the job natively or in Docker
    if (args.native):
        os.system(extensionCommands[ext] + runJob.source + " " + arguments + " " + params)
    else:
        drun(config, runJob, arguments, params, args.skip_build)
