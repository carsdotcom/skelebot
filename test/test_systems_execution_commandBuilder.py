from unittest import TestCase
from unittest import mock
from argparse import Namespace

import skelebot as sb
import os

class TestCommandBuilder(TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()


    @mock.patch('os.getcwd')
    def test_build_ephemeral(self, mock_getcwd):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]

        expected = "./build.sh 0.1 --env local"
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        self.assertEqual(command, expected)


if __name__ == '__main__':
    unittest.main()
