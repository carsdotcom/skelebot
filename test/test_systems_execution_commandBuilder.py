import os
import unittest
from unittest import mock
from argparse import Namespace

import skelebot as sb

class TestCommandBuilder(unittest.TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_build(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1', test=True)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        param = sb.objects.param.Param("test", "t", accepts="boolean")
        job.params.append(param)

        expected = "bash build.sh 0.1 --env local --test --log info"
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        self.assertEqual(command, expected)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_build_no_boolean(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='1.1')

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        param = sb.objects.param.Param("test", "t", accepts="boolean")
        job.params.append(param)

        expected = "bash build.sh 1.1 --env local --log info"
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        self.assertEqual(command, expected)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_direct_command(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[1]

        expected = "echo Hello"
        command = sb.systems.execution.commandBuilder.build(config, job, None)
        self.assertEqual(command, expected)

if __name__ == '__main__':
    unittest.main()
