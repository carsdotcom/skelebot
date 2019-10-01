"""Command Builder"""

from ...common import EXT_COMMAND

COMMAND = "{pre}{extCommand}{file}{params}{post}"

def build(config, job, args, native=False):
    """Build the command that will either be executed via Docker, or on the native system"""

    ext_list = job.source.split()[0].split(".")
    if len(ext_list) == 1:
        ext = "None"
    else:
        ext = ext_list[-1]

    args = {} if args is None else vars(args)
    arguments = ""
    pre = ""
    post = ""

    # Build the params list from the args and params of the job with the supplied values
    params = buildArgs(job.args, args)
    params += buildParams(job.params, args)
    # Global parameters are ignored, if the direct command is specified in the job source
    if not ext == "None":
        params += buildParams(config.params, args)

    # Construct the pre-run and post-run commands from the components
    for component in config.components:
        preCmd = component.prependCommand(job, native)
        postCmd = component.appendCommand(job, native)
        if (preCmd is not None):
            pre += "{cmd} && ".format(cmd=preCmd)
        if (postCmd is not None):
            post += " && {cmd}".format(cmd=postCmd)

    command = COMMAND.format(extCommand=EXT_COMMAND[ext], file=job.source, args=arguments,
                             params=params, pre=pre, post=post)
    return command

def buildArgs(argParams, args):
    """Build the list of arguments that are passed through to the command"""

    argString = ""
    if (argParams is not None):
        for arg in argParams:
            value = args.get(arg.name)
            if (value is not None):
                argString += " {}".format(value)

    return argString

def buildParams(jobParams, args):
    """Build the list of parameters that are passed through to the command"""

    paramString = ""
    if (jobParams is not None):
        for param in jobParams:
            value = args.get(param.name, param.default)
            if (param.accepts == "boolean"):
                if (value):
                    paramString += " --{name}".format(name=param.name)
            elif (value is not None):
                paramString += " --{name} {value}".format(name=param.name, value=value)

    return paramString
