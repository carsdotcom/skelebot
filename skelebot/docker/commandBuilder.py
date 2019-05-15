from ..common import EXT_COMMAND

COMMAND = "{pre}{extCommand}{file} {args} {params}{post}"

def build(config, job, args, native=False):

    ext = job.source.split(".")[1]
    arguments = ""
    params = ""
    pre = ""
    post = ""

    # Construct the string of arguments
    if (job.args != None):
        for arg in job.args:
            value = vars(args)[arg.name]
            if (value == None):
                value = arg.default
            if (value != None):
                arguments = arguments + value + " "

    # Construct the string of parameters
    if (job.params != None):
        for param in job.params:
            value = vars(args)[param.name]
            if (value == None):
                value = param.default
            if (value != None):
                params = params + "--" + param.name + " " + value + " "

    # Construct the pre-run and post-run commands from the components
    for component in components:
        preCmd = component.prependCommand(job, native)
        postCmd = component.appendCommand(job, native)
        if (preCmd is not None):
            pre += "{cmd} && ".format(cmd=preCmd)
        if (postCmd is not None):
            post += " && {cmd}".format(cmd=postCmd)

    return COMMAND.format(extCommand=EXT_COMMAND[ext], file=job.source, args=arguments, params=params, pre=pre, post=post)
