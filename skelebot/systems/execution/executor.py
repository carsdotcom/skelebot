from ..scaffolding.scaffolder import scaffold
import os

def executeJob(config, args):
    # Execute the job or start scaffolding (print help if no command provided)
    # [TODO] Switch Statements, ever heard of them?
    if (args.job == None):
        parser.print_help()
    elif (args.job == "scaffold"):
        scaffold(args.existing)
    else:
        # Check to see if the job command matches a job name
        job = None
        for configJob in config.jobs:
            if args.job == configJob.name:
                job = configJob

        if (job is not None):
            # Execute the Job
            command = commandBuilder.build(config, job, args, args.native)
            if (args.native):
                # Execute the job natively
                os.system(command)
            else:
                # Execute the job in Docker
                if (args.skip_build == False):
                    docker.build(config)
                docker.run(config, command, job.mode, config.ports, job.mappings, job.name)
