def buildDockerignore(config, job=None):
    dockerignore = ""

    if (config.ignore != None):
        dockerignore = "\n".join(config.ignore)

    if (job != None):
        if (job.ignore != None):
            dockerignore += "\n"
            dockerignore += "\n".join(job.ignore)

    return dockerignore
