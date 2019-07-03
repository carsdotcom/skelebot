from .systems.parsing import skeleParser
from .systems.generators import yaml
from .systems.execution import executor, docker, commandBuilder
import sys

# The main function for Skelebot CLI where the config is loaded, arguments are parsed, and commands are executed
def main():

    # Parse the env manually in order to read the correct yaml configuration
    args = sys.argv
    env = None
    for index in range(len(args)-1):
        if (args[index] == "-e") or (args[index] == "--env"):
            env = args[index+1]

    config = yaml.loadConfig(env)
    sbParser = skeleParser.SkeleParser(config, env)
    status = executor.execute(config, sbParser)
