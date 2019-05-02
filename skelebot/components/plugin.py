from ..objects.component import Component

class Plugin(Component):
    
    # Add a parser for the plugin command with a single argument for the plugin's zip file
    def addParsers(self, subparsers):
        parser = subparsers.add_parser("plugin", help="Install a plugin for skelebot from a local zip file")
        parser.add_argument("plugin", help="The zip file of the skelebot plugin")
        return subparsers
