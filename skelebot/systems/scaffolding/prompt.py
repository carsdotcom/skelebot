"""Prompt Function"""

def promptUser(message, options=None, boolean=False):
    """Construct dynamic prompts for user input and return the user-entered value"""

    inp = None

    if (options):
        options = list(map(str, options))
        while inp not in options:
            inp = input("{msg} [{options}]: ".format(msg=message, options=', '.join(options)))
    elif (boolean):
        inp = input("{msg} [Y/N]: ".format(msg=message)) in ["Y", "y"]
    else:
        inp = input("{msg}: ".format(msg=message))

    return inp
