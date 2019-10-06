import argparse
import os
import unittest
from unittest import mock

import skelebot as sb

class TestBump(unittest.TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    def test_addParsers(self):
        bump = sb.components.bump.Bump()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = bump.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["bump"], None)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_execute_major(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()
        args = argparse.Namespace(version='major')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpVersion = sb.systems.generators.yaml.loadVersion()
        sb.systems.generators.yaml.saveVersion("6.6.6")

        self.assertEqual(bumpVersion, "7.0.0")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_execute_minor(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()
        args = argparse.Namespace(version='minor')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpVersion = sb.systems.generators.yaml.loadVersion()
        sb.systems.generators.yaml.saveVersion("6.6.6")

        self.assertEqual(bumpVersion, "6.7.0")


    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_execute_patch(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()
        args = argparse.Namespace(version='patch')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpVersion = sb.systems.generators.yaml.loadVersion()
        sb.systems.generators.yaml.saveVersion("6.6.6")

        self.assertEqual(bumpVersion, "6.6.7")

if __name__ == '__main__':
    unittest.main()
