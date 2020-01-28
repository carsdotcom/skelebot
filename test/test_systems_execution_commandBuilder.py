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

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_build_short_param(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[2]
        param = sb.objects.param.Param("test", "t", accepts="boolean")
        job.params.append(param)

        expected = "bash test_short.sh -f csv --log info"
        command = sb.systems.execution.commandBuilder.build(config, job, None)
        self.assertEqual(command, expected)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_build_kabob_params(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1', test_test="test", arg_arg="argy")

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        param = sb.objects.param.Param("test-test", "t")
        arg = sb.objects.arg.Arg("arg-arg")
        job.params.append(param)
        job.args.append(arg)

        expected = "bash build.sh 0.1 argy --env local --test-test test --log info"
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        self.assertEqual(command, expected)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_build_list_param(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1', test_test=[1, 2, 3], arg_arg="argy")

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        param = sb.objects.param.Param("test-test", "t", accepts="list")
        arg = sb.objects.arg.Arg("arg-arg")
        job.params.append(param)
        job.args.append(arg)

        expected = "bash build.sh 0.1 argy --env local --test-test 1 2 3 --log info"
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        self.assertEqual(command, expected)

if __name__ == '__main__':
    unittest.main()
