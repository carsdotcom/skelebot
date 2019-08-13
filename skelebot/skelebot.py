"""Skelebot - Machine Learning Project Management Tool"""

import sys
from schema import SchemaError
from .systems.parsing import skeleParser
from .systems.generators import yaml
from .systems.execution import executor

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
        print("\u001b[0m\u001b[31mERROR | skelebot.yaml |", error, "\u001b[0m")
        exit(1)

def get_env():
    """Parse the env manually in order to read the correct yaml configuration"""

    args = sys.argv
    env = None
    for index in range(len(args)-1):
        if (args[index] == "-e") or (args[index] == "--env"):
            env = args[index+1]

    return env
