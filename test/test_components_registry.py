import argparse
import copy
import unittest
from unittest import mock

from schema import SchemaError

import skelebot as sb

class TestRegistry(unittest.TestCase):

    registry = {
        "host": "docker.io",
        "port": 88,
        "user": "skelebot"
    }

    def test_addParsers(self):
        registry = sb.components.registry.Registry(host="docker.io", port=88, user="skelebot")

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = registry.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["publish"], None)

    @mock.patch('skelebot.components.registry.docker')
    def test_execute(self, mock_docker):
        mock_docker.build.return_value = 0

        config = sb.objects.config.Config(language="R")
        args = argparse.Namespace()

        registry = sb.components.registry.Registry(host="docker.io", port=88, user="skelebot")
        registry.execute(config, args)

        mock_docker.login.assert_called_with("docker.io")
        mock_docker.build.assert_called_with(config)
        mock_docker.push.assert_called_with(config, "docker.io", 88, "skelebot")

    def test_validate_valid(self):
        try:
            sb.components.registry.Registry.validate(self.registry)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def validate_error(self, attr, reset, expected):
        registry = copy.deepcopy(self.registry)
        registry[attr] = reset

        try:
            sb.components.registry.Registry.validate(registry)
        except SchemaError as error:
            self.assertEqual(error.code, "Registry '{attr}' must be a{expected}".format(attr=attr, expected=expected))

    def test_invalid(self):
        self.validate_error('host', 123, ' String')
        self.validate_error('port', "abc", 'n Integer')
        self.validate_error('user', 123, ' String')

if __name__ == '__main__':
    unittest.main()
