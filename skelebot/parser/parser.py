import argparse
from argparse import RawTextHelpFormatter

DESCRIPTION = """
\033[1m{project}\033[0m
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version (project): {sbVersion}
Skelebot Version (installed): {version}
-----------------------------------"""

class Parser():

    def __init__(self, config=None):
        # Obtain the env manually from the args
        isNext = False
        env = None
        for arg in sys.argv:
            if (isNext):
                env = arg
                isNext = False
            if (arg == "-e") or (arg == "--env"):
                isNext = True

        desc = "Skelebot Version: {version}".format(version=VERSION)
        if (config != None):
            name = " ".join([word.capitalize() for word in config.name.split("-")])
            desc = config.description
            version = config.version
            sbVersion = config.skelebotVersion
            desc = DESCRIPTION.format(sbVersion=sbVersion, version=VERSION, project=name, desc=desc, pVersion=version, env=env)

        parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")


        # Add the plugin command for installing new skelebot plugins from zip files
        pluginParser = subparsers.add_parser("plugin", help="Install a plugin for skelebot from a local zip file")
        pluginParser.add_argument("plugin", help="The zip file of the skelebot plugin")

    def parseArgs(self):

