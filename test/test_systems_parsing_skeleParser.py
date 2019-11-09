import unittest
from unittest import mock

from colorama import Style

import skelebot as sb

class TestParser(unittest.TestCase):

    def test_parseArgs(self):
        arg1 = sb.objects.arg.Arg(name="start")
        arg2 = sb.objects.arg.Arg(name="end", choices=["now", "never"])
        param1 = sb.objects.param.Param(name="days", alt="d", default=10)
        param2 = sb.objects.param.Param(name="env", alt="e", default="local", choices=["local", "prod"])
        param3 = sb.objects.param.Param(name="method", accepts="boolean")
        param4 = sb.objects.param.Param(name="simple")
        param4 = sb.objects.param.Param(name="multi", accepts="list")
        topParam = sb.objects.param.Param(name="log", alt="l", default="info", choices=["debug", "info", "warn", "error"])
        job = sb.objects.job.Job(name="test", mode="d", source="test.py", help="TEST", args=[arg1, arg2], params=[param1, param2, param3, param4])
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0", jobs=[job], params=[topParam])
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs(["test", "2019", "never", "-d", "20", "--env", "prod", "-l", "debug", "--method", "--multi", "abc", "123"])

        self.assertEqual(args.job, "test")
        self.assertEqual(args.start, "2019")
        self.assertEqual(args.end, "never")
        self.assertEqual(args.days, "20")
        self.assertEqual(args.env, "prod")
        self.assertEqual(args.log, "debug")
        self.assertEqual(args.method, True)
        self.assertEqual(args.multi, ["abc", "123"])
        self.assertEqual(hasattr(args, 'simple'), False)

    def test_parseArgs_non_skelebot_scaffold(self):
        config = sb.objects.config.Config()
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs(["scaffold"])

        self.assertEqual(args.job, "scaffold")
        self.assertEqual(args.existing, False)

    @mock.patch('skelebot.systems.parsing.skeleParser.VERSION', '6.6.6')
    def test_description(self):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0")
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        description = sbParser.desc

        expectedDescription = Style.BRIGHT + "Test Project" + Style.RESET_ALL + """
A test project
-----------------------------------
Version: 0.1.0
Environment: test
Skelebot Version: 6.6.6
-----------------------------------"""

        self.assertEqual(description, expectedDescription)

    @mock.patch('skelebot.systems.parsing.skeleParser.argparse.ArgumentParser.print_help')
    def test_help(self, mock_printHelp):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0")
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        actualHelp = sbParser.showHelp()

        mock_printHelp.expect_called_once_with()

    def test_parse_component_args(self):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0", components=[sb.components.plugin.Plugin()])
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config)
        args = sbParser.parseArgs(["plugin", "pg.zip"])

        self.assertEqual(args.plugin, "pg.zip")

if __name__ == '__main__':
    unittest.main()
