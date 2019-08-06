from skelebot.objects.component import *

# Just a dummy plugin for testing
class AddNumbers(Component):
    activation = Activation.ALWAYS
    commands = ["addNumbers"]

    def addParsers(self, subparsers):
       subparsers.add_parser("addNumbers", help="adds the numbers 1 and 2 to get 3!")
       return subparsers

    def execute(self, config, args):
        a = 1
        b = 2
        print(a, " + ", b, " = ", a + b)
