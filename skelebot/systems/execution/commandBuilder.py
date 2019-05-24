from ...common import EXT_COMMAND

COMMAND = "{pre}{extCommand}{file}{params}{post}"

def build(config, job, args, native=False):

    ext = job.source.split(".")[1]
    args = vars(args)
    arguments = ""
    pre = ""
    post = ""

    # Build the params list from the args and params of the job with the supplied values (or defaults)
    params = buildArgs(job.args, args, " {value}")
    params += buildArgs(job.params, args, " --{name} {value}")

    # Construct the pre-run and post-run commands from the components
    for component in config.components:
        preCmd = component.prependCommand(job, native)
        postCmd = component.appendCommand(job, native)
        if (preCmd is not None):
            pre += "{cmd} && ".format(cmd=preCmd)
        if (postCmd is not None):
            post += " && {cmd}".format(cmd=postCmd)

    return COMMAND.format(extCommand=EXT_COMMAND[ext], file=job.source, args=arguments, params=params, pre=pre, post=post)

def buildArgs(jobArgs, args, template):
    argString = ""
    if (jobArgs != None):
        for arg in jobArgs:
            value = args[arg.name] if (arg.name in args) else arg.default
            if (value != None):
                argString += template.format(name=arg.name, value=value)

    return argString
