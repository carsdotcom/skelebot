import os

def executeJob(config, args):
    # Identify the job to run
    runJob = None
    for job in config.jobs:
        if args.job == job.name:
            runJob = job

    # Execute the job natively or in Docker
    command = commandBuilder.build(config, runJob, args, args.native)
    if (args.native):
        os.system(command)
    else:
        if (args.skip_build == False):
            docker.build(config)
        docker.run(config, job, command)
