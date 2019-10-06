import copy
import unittest

from schema import SchemaError

import skelebot as sb

class TestArgValidate(unittest.TestCase):

    arg = {
        'name': 'test',
        'help': 'test',
        'choices': [1, 2]
    }

    def validate_error(self, attr, reset, expected):
        arg = copy.deepcopy(self.arg)
        arg[attr] = reset

        try:
            sb.objects.arg.Arg.validate(arg)
        except SchemaError as error:
            self.assertEqual(error.code, "Arg '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def test_valid(self):

        try:
            sb.objects.arg.Arg.validate(self.arg)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_invalid_mising(self):
        arg = copy.deepcopy(self.arg)
        del arg['name']

        try:
            sb.objects.arg.Arg.validate(arg)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing key: 'name'")

    def test_invalid(self):
        self.validate_error('name', 123, 'String')
        self.validate_error('help', 123, 'String')
        self.validate_error('choices', 123, 'List')

if __name__ == '__main__':
    unittest.main()
