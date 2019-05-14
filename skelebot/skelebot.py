from .parser import parser
from .files import yaml
from .scaffolding import scaffolder
import sys

# [TODO] Move this to the env System
# Obtain the environment parameter from the skelebot command string prior to contructing the arg parser
def getEnvironment():
    isNext = False
    env = None
    for arg in sys.argv:
        if (isNext):
            env = arg
            break

        if (arg == "-e") or (arg == "--env"):
            isNext = True

    return env

# The main function for Skelebot CLI where the config is loaded, arguments are parsed, and commands are executed
def main():

    env = getEnvironment()
    config = yaml.loadConfig(env)
    args = parser.parseArgs(config, env)

    scaffolder.scaffold()
