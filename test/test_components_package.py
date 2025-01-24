import copy
import argparse
import unittest
from unittest import mock

from schema import SchemaError

import skelebot as sb

class TestPlugin(unittest.TestCase):

    package_yaml = {
        "path": "test.zip",
        "ignores": ["one.txt", "two.txt"]
    }

    def test_addParsers(self):
        package = sb.components.package.Package()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = package.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["package"], None)

    @mock.patch('skelebot.components.package.call')
    def test_execute(self, mock_call):
        mock_call.return_value = 0

        config = sb.objects.config.Config()
        args = argparse.Namespace()

        package = sb.components.package.Package(path="test.zip")
        package.execute(config, args)

        mock_call.assert_called_once_with("zip -r test.zip .", shell=True)

    @mock.patch('os.remove')
    @mock.patch('os.path.exists')
    @mock.patch('skelebot.components.package.call')
    def test_execute_existing(self, mock_call, mock_exists, mock_remove):
        mock_call.return_value = 0
        mock_exists.return_value = True

        config = sb.objects.config.Config()
        args = argparse.Namespace()

        package = sb.components.package.Package(path="test.zip")
        package.execute(config, args)

        mock_call.assert_called_once_with("zip -r test.zip .", shell=True)
        mock_exists.assert_called_once_with("test.zip")
        mock_remove.assert_called_once_with("test.zip")

    @mock.patch('skelebot.components.package.call')
    def test_execute_ignores(self, mock_call):
        mock_call.return_value = 0

        config = sb.objects.config.Config()
        args = argparse.Namespace()

        package = sb.components.package.Package(path="test.zip", ignores=[r"folder/**\*", "file.txt"])
        package.execute(config, args)

        mock_call.assert_called_once_with(r"zip -r test.zip . -x folder/**\* file.txt", shell=True)

    def test_validate_valid(self):
        try:
            sb.components.package.Package.validate(self.package_yaml)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def validate_error(self, attr, reset, expected):
        package_yaml = copy.deepcopy(self.package_yaml)
        package_yaml[attr] = reset

        try:
            sb.components.package.Package.validate(package_yaml)
        except SchemaError as error:
            self.assertEqual(error.code, "Package '{attr}' must be a{expected}".format(attr=attr, expected=expected))

    def test_invalid(self):
        self.validate_error('path', 123, ' String')
        self.validate_error('ignores', 123, ' List')

if __name__ == '__main__':
    unittest.main()
