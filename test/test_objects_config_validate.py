import copy
import unittest
from unittest import mock

from colorama import Fore, Style

from schema import SchemaError

import skelebot as sb

class TestConfigValidate(unittest.TestCase):

    config = {
        'name': 'test',
        'env': 'test',
        'description': 'test',
        'maintainer': 'test',
        'contact': 'test',
        'baseImage': 'test',
        'primaryJob': 'test',
        'host': 'test',
        'ephemeral': True,
        'dependencies': [1, 2],
        'ignores': [1, 2],
        'jobs': [1, 2],
        'ports': [1, 2],
        'components': {},
        'params': [1, 2],
        'commands': [],
        'pythonVersion': '3.9',
        'gpu': True
    }

    def validate_error(self, attr, reset, expected):
        config = copy.deepcopy(self.config)
        config[attr] = reset

        try:
            sb.objects.config.Config.validate(config)
        except SchemaError as error:
            self.assertEqual(error.code, "'{attr}' must be {expected}".format(attr=attr, expected=expected))

    def test_valid(self):

        try:
            sb.objects.config.Config.validate(self.config)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    @mock.patch.object(sb.objects.config, 'DEPRECATED_VERSIONS', ['3.6'])
    @mock.patch('skelebot.objects.config.print')
    def test_valid_deprecated(self, mock_print):
        _ = sb.objects.config.Config(pythonVersion='3.6')
        mock_print.assert_called_once_with(
            Fore.YELLOW + "WARN" + Style.RESET_ALL
            + " | The support for Python version 3.6 has been deprecated as of v1.37.0."
            + " Please use a higher version."
        )

    def test_invalid_mising(self):
        config = copy.deepcopy(self.config)
        del config['name']

        try:
            sb.objects.config.Config.validate(config)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing key: 'name'")

    def test_invalid(self):
        self.validate_error('name', 123, 'a String')
        self.validate_error('env', 123, 'a String')
        self.validate_error('description', 123, 'a String')
        self.validate_error('maintainer', 123, 'a String')
        self.validate_error('contact', 123, 'a String')
        self.validate_error('baseImage', 123, 'a String')
        self.validate_error('primaryJob', 123, 'a String')
        self.validate_error('primaryExe', 123, 'CMD or ENTRYPOINT')
        self.validate_error('primaryExe', 'bad', 'CMD or ENTRYPOINT')
        self.validate_error('ephemeral', 123, 'a Boolean')
        self.validate_error('dependencies', 123, 'a Dict or List')
        self.validate_error('ignores', 123, 'a List')
        self.validate_error('jobs', 123, 'a List')
        self.validate_error('ports', 123, 'a List')
        self.validate_error('components', 123, 'a Dictionary')
        self.validate_error('params', 123, 'a List')
        self.validate_error('commands', 123, 'a List')
        self.validate_error('host', 123, 'a String')
        self.validate_error('pythonVersion', 123, 'one of:' + ', '.join(sb.common.PYTHON_VERSIONS))
        self.validate_error('gpu', 123, 'a Boolean')

if __name__ == '__main__':
    unittest.main()
