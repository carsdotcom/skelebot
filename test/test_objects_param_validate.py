import copy
import unittest

from schema import SchemaError

import skelebot as sb

class TestParamValidate(unittest.TestCase):

    param = {
        'name': 'test',
        'alt': 'test',
        'accepts': 'test',
        'default': 'test',
        'help': 'test',
        'choices': [1, 2]
    }

    def validate_error(self, attr, reset, expected):
        param = copy.deepcopy(self.param)
        param[attr] = reset

        try:
            sb.objects.param.Param.validate(param)
        except SchemaError as error:
            self.assertEqual(error.code, "Param '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def test_valid(self):

        try:
            sb.objects.param.Param.validate(self.param)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_invalid_mising(self):
        param = copy.deepcopy(self.param)
        del param['name']

        try:
            sb.objects.param.Param.validate(param)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing key: 'name'")

    def test_invalid(self):
        self.validate_error('name', 123, 'String')
        self.validate_error('alt', 123, 'String')
        self.validate_error('accepts', 123, 'String')
        self.validate_error('help', 123, 'String')
        self.validate_error('choices', 123, 'List')

if __name__ == '__main__':
    unittest.main()
