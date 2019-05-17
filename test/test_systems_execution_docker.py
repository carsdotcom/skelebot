from unittest import TestCase
from unittest import mock
from argparse import Namespace

import skelebot as sb
import os

class TestDocker(TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.remove')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_ephemeral(self, mock_getcwd, mock_system, mock_remove):
        folderPath = "{path}/test/files".format(path=self.path)
        dockerignorePath = "{folder}/.dockerignore".format(folder=folderPath)
        dockerfilePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_getcwd.return_value = folderPath
        mock_system.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()
        config.ephemeral = True

        status = sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test .")
        mock_remove.assert_any_call("Dockerfile")
        mock_remove.assert_any_call(".dockerignore")
        self.assertEqual(status, 1)

    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_non_ephemeral(self, mock_getcwd, mock_system):
        folderPath = "{path}/test/files".format(path=self.path)
        dockerignorePath = "{folder}/.dockerignore".format(folder=folderPath)
        dockerfilePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_getcwd.return_value = folderPath
        mock_system.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()

        status = sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test .")
        self.assertEqual(status, 1)

    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_run(self, mock_getcwd, mock_system):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        mock_getcwd.return_value = folderPath
        mock_system.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-build --rm -i -v $PWD/data/:/app/data/ -v $PWD/output/:/app/output/ -v $PWD/temp/:/app/temp/ test /bin/bash -c './build.sh 0.1 --env local'"
        status = sb.systems.execution.docker.run(config, job, command)
        mock_system.assert_called_once_with(expected)
        self.assertEqual(status, 1)

if __name__ == '__main__':
    unittest.main()
