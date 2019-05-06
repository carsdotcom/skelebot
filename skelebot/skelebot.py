from .parser import parser
from .files import yaml

def main():

    config = yaml.loadConfig()
    args = parser.parseArgs(config)
