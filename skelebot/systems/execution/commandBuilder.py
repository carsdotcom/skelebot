from ...common import EXT_COMMAND

COMMAND = "{pre}{extCommand}{file}{params}{post}"

def build(config, job, args, native=False):

    ext = job.source.split(".")[1]
    args = vars(args)
    arguments = ""
    pre = ""
    post = ""

    # Build the params list from the args and params of the job with the supplied values (or defaults)
    params = buildArgs(job.args, args)
    params += buildParams(job.params, args)
    params += buildParams(config.params, args)

    # Construct the pre-run and post-run commands from the components
    for component in config.components:
        preCmd = component.prependCommand(job, native)
        postCmd = component.appendCommand(job, native)
        if (preCmd is not None):
            pre += "{cmd} && ".format(cmd=preCmd)
        if (postCmd is not None):
            post += " && {cmd}".format(cmd=postCmd)

    return COMMAND.format(extCommand=EXT_COMMAND[ext], file=job.source, args=arguments, params=params, pre=pre, post=post)

def buildArgs(argParams, args):
    argString = ""
    if (argParams != None):
        for arg in argParams:
            value = args.get(arg.name)
            if (value != None):
                argString += " {}".format(value)

    return argString

def buildParams(jobParams, args):
    paramString = ""
    if (jobParams != None):
        for param in jobParams:
            value = args.get(param.name, param.default)
            if (param.accepts == "boolean"):
                if (value == True):
                    paramString += " --{name}".format(name=param.name)
            elif (value != None):
                paramString += " --{name} {value}".format(name=param.name, value=value)

    return paramString
