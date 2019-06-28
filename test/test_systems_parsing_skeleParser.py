from unittest import TestCase
from unittest import mock

import skelebot as sb
import os

class TestParser(TestCase):

    def test_parseArgs(self):
        arg1 = sb.objects.param.Param(name="start")
        arg2 = sb.objects.param.Param(name="end", choices=["now", "never"])
        param1 = sb.objects.param.Param(name="days", alt="d", default=10)
        param2 = sb.objects.param.Param(name="env", alt="e", default="local", choices=["local", "prod"])
        job = sb.objects.job.Job(name="test", mode="d", source="test.py", help="TEST", args=[arg1, arg2], params=[param1, param2])
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0", jobs=[job])
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs(["test", "2019", "never", "-d", "20", "--env", "prod"])

        argKeys = list(vars(args).keys())
        self.assertEqual(args.job, "test")
        self.assertEqual(args.start, "2019")
        self.assertEqual(args.end, "never")
        self.assertEqual(args.days, "20")
        self.assertEqual(args.env, "prod")

    def test_parseArgs_non_skelebot_scaffold(self):
        config = sb.objects.config.Config()
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs(["scaffold"])

        argKeys = list(vars(args).keys())
        self.assertEqual(args.job, "scaffold")
        self.assertEqual(args.existing, False)

    def test_description(self):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0")
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        description = sbParser.desc

        expectedDescription = """
\033[1mTest Project\033[0m
A test project
-----------------------------------
Version: 0.1.0
Environment: test
Skelebot Version: 0.2.13
-----------------------------------"""

        self.assertEqual(description, expectedDescription)

if __name__ == '__main__':
    unittest.main()
