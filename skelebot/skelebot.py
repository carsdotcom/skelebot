"""Skelebot - Machine Learning Project Development Tool"""

import sys
from colorama import Fore, Style
from schema import SchemaError
from .systems.parsing import skeleParser
from .systems.generators import yaml
from .systems.execution import executor


ERROR_HEADER = Fore.RED + "ERROR" + Style.RESET_ALL
ERROR = ERROR_HEADER + " | {}"
SCHEMA_ERROR = ERROR_HEADER + " | skelebot.yaml | {}"

def main():
    """
    The main function for Skelebot CLI where the config is loaded,
    arguments are parsed, and commands are executed
    """

    try:
        env = get_env()
        config = yaml.loadConfig(env)
        parser = skeleParser.SkeleParser(config, env)
        executor.execute(config, parser)
    except SchemaError as error:
        print(SCHEMA_ERROR.format(error))
        sys.exit(1)
    except RuntimeError as error:
        print(ERROR.format(error))
        sys.exit(1)

def get_env():
    """Parse the env manually in order to read the correct yaml configuration"""

    env = None
    prevArg = None
    baseArgs = {None, "-s", "--skip-build", "-n", "--native"}
    for arg in sys.argv:
        if (prevArg == "-e") or (prevArg == "--env"):
            env = arg
            break
        elif (prevArg not in baseArgs) and (prevArg.endswith("skelebot") == False):
            break
        else:
            prevArg = arg

    return env
