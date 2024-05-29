"""Prompt Function"""

def promptUser(message, options=None, boolean=False, deprecated_options=None):
    """Construct dynamic prompts for user input and return the user-entered value"""

    inp = None
    if deprecated_options is None:
        deprecated_options = []

    if (options):
        options = list(map(str, options))
        p_options = []
        for o in options:
            p_options.append(o + " (DEPRECATED)" if o in deprecated_options else o)
        if (len(options) == 1):
            inp = options[0]
        while inp not in options:
            inp = input("{msg} [{options}]: ".format(msg=message, options=', '.join(p_options)))
    elif (boolean):
        inp = input("{msg} [Y/N]: ".format(msg=message)) in ["Y", "y"]
    else:
        inp = input("{msg}: ".format(msg=message))

    return inp
