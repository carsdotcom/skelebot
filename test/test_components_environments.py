import argparse
import copy
import unittest
from unittest import mock

from schema import SchemaError

import skelebot as sb

class TestEnvironments(unittest.TestCase):

    def test_addParsers(self):
        environments = sb.components.environments.Environments()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = environments.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["envs"], None)

    @mock.patch('skelebot.components.environments.print')
    def test_execute(self, mock_print):
        config = sb.objects.config.Config()
        args = argparse.Namespace()

        environments = sb.components.environments.Environments()
        res = environments.execute(config, args)

        self.assertEqual(res, 0)
        mock_print.assert_has_calls([mock.call("[default]"), mock.call("exp")])

if __name__ == '__main__':
    unittest.main()
