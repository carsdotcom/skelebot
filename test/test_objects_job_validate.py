import copy
import unittest

from schema import SchemaError

import skelebot as sb

class TestJobValidate(unittest.TestCase):

    job = {
        'name': 'test',
        'source': 'test',
        'mode': 'test',
        'native': 'optional',
        'help': 'test',
        'args': [1, 2],
        'params': [1, 2],
        'ignores': [1, 2],
        'mappings': [1, 2]
    }

    def validate_error(self, attr, reset, expected):
        job = copy.deepcopy(self.job)
        job[attr] = reset

        try:
            sb.objects.job.Job.validate(job)
            self.fail("Exception Expected")
        except SchemaError as error:
            self.assertEqual(error.code, "Job '{attr}' must be {expected}".format(attr=attr, expected=expected))

    def test_valid(self):

        try:
            sb.objects.job.Job.validate(self.job)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_invalid_mising(self):
        job = copy.deepcopy(self.job)
        del job['name']
        del job['source']
        del job['help']

        try:
            sb.objects.job.Job.validate(job)
            self.fail("Exception Expected")
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'help', 'name', 'source'")

    def test_invalid(self):
        self.validate_error('name', 123, 'a String')
        self.validate_error('source', 123, 'a String')
        self.validate_error('mode', 123, 'a String')
        self.validate_error('native', 'nope', 'one of: \'always\', \'never\', \'optional\'')
        self.validate_error('help', 123, 'a String')
        self.validate_error('args', 123, 'a List')
        self.validate_error('params', 123, 'a List')
        self.validate_error('ignores', 123, 'a List')
        self.validate_error('mappings', 123, 'a List')

if __name__ == '__main__':
    unittest.main()
