import copy
import unittest

from schema import SchemaError

import skelebot as sb

class TestConfigValidate(unittest.TestCase):

    config = {
        'name': 'test',
        'env': 'test',
        'description': 'test',
        'maintainer': 'test',
        'contact': 'test',
        'language': 'test',
        'baseImage': 'test',
        'primaryJob': 'test',
        'ephemeral': True,
        'dependencies': [1, 2],
        'ignores': [1, 2],
        'jobs': [1, 2],
        'ports': [1, 2],
        'components': {},
        'params': [1, 2],
        'commands': [],
    }

    def validate_error(self, attr, reset, expected):
        config = copy.deepcopy(self.config)
        config[attr] = reset

        try:
            sb.objects.config.Config.validate(config)
        except SchemaError as error:
            self.assertEqual(error.code, "'{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def test_valid(self):

        try:
            sb.objects.config.Config.validate(self.config)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_invalid_mising(self):
        config = copy.deepcopy(self.config)
        del config['name']
        del config['language']

        try:
            sb.objects.config.Config.validate(config)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'language', 'name'")

    def test_invalid(self):
        self.validate_error('name', 123, 'String')
        self.validate_error('env', 123, 'String')
        self.validate_error('description', 123, 'String')
        self.validate_error('maintainer', 123, 'String')
        self.validate_error('contact', 123, 'String')
        self.validate_error('language', 123, 'String')
        self.validate_error('baseImage', 123, 'String')
        self.validate_error('primaryJob', 123, 'String')
        self.validate_error('ephemeral', 123, 'Boolean')
        self.validate_error('dependencies', 123, 'List')
        self.validate_error('ignores', 123, 'List')
        self.validate_error('jobs', 123, 'List')
        self.validate_error('ports', 123, 'List')
        self.validate_error('components', 123, 'Dictionary')
        self.validate_error('params', 123, 'List')
        self.validate_error('commands', 123, 'List')

if __name__ == '__main__':
    unittest.main()
