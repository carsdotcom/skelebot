from unittest import TestCase
from unittest import mock

import skelebot as sb
import os

class TestParser(TestCase):

    def test_parseArgs(self):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0", skelebotVersion="0.2.0")
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs()

        argKeys = list(vars(args).keys())
        self.assertEqual(argKeys, ["job", "env", "skip_build", "native"])

    def test_parseArgs_non_skelebot(self):
        config = sb.objects.config.Config()
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        args = sbParser.parseArgs()

        argKeys = list(vars(args).keys())
        self.assertEqual(argKeys, ["job"])


    def test_description(self):
        config = sb.objects.config.Config(name="test-project", description="A test project", version="0.1.0", skelebotVersion="0.2.0")
        sbParser = sb.systems.parsing.skeleParser.SkeleParser(config, "test")
        description = sbParser.desc

        expectedDescription = """
\033[1mTest Project\033[0m
A test project
-----------------------------------
Version: 0.1.0
Environment: test
Skelebot Version (project): 0.2.0
Skelebot Version (installed): 0.2.1
-----------------------------------"""

        self.assertEqual(description, expectedDescription)

if __name__ == '__main__':
    unittest.main()
