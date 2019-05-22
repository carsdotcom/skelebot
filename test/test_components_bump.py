from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os

class TestBump(TestCase):
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
        ogVersion = config.version
        args = argparse.Namespace(version='major')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpConfig = sb.systems.generators.yaml.loadConfig()
        self.assertEqual(config.version, "7.0.0")

        config.version = ogVersion
        sb.systems.generators.yaml.saveConfig(config)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_execute_minor(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()
        ogVersion = config.version
        args = argparse.Namespace(version='minor')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpConfig = sb.systems.generators.yaml.loadConfig()
        self.assertEqual(config.version, "6.7.0")

        config.version = ogVersion
        sb.systems.generators.yaml.saveConfig(config)
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_execute_patch(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()
        ogVersion = config.version
        args = argparse.Namespace(version='patch')

        bump = sb.components.bump.Bump()
        bump.execute(config, args)

        bumpConfig = sb.systems.generators.yaml.loadConfig()
        self.assertEqual(config.version, "6.6.7")

        config.version = ogVersion
        sb.systems.generators.yaml.saveConfig(config)

if __name__ == '__main__':
    unittest.main()
