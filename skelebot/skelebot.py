from .systems.parsing import skeleParser
from .systems.generators import yaml
from .systems.execution import executor, docker, commandBuilder
import sys

# Obtain the environment parameter from the skelebot command string prior to contructing the arg parser
def getEnvironment(args):
    env = None
    for index in range(len(args)-1):
        if (args[index] == "-e") or (args[index] == "--env"):
            env = args[index+1]

    return env

# The main function for Skelebot CLI where the config is loaded, arguments are parsed, and commands are executed
def main():

    env = getEnvironment(sys.argv)
    config = yaml.loadConfig(env)
    sbParser = skeleParser.SkeleParser(config, env)
    status = executor.execute(config, sbParser)
