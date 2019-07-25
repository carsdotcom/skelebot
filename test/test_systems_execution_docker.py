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

    @mock.patch('os.path.expanduser')
    @mock.patch('os.remove')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_ephemeral(self, mock_getcwd, mock_system, mock_remove, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        dockerignorePath = "{folder}/.dockerignore".format(folder=folderPath)
        dockerfilePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.ephemeral = True

        sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test .")
        mock_remove.assert_any_call("Dockerfile")
        mock_remove.assert_any_call(".dockerignore")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_non_ephemeral(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        dockerignorePath = "{folder}/.dockerignore".format(folder=folderPath)
        dockerfilePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test .")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_error(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        dockerignorePath = "{folder}/.dockerignore".format(folder=folderPath)
        dockerfilePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()

        with self.assertRaisesRegex(Exception, "Docker Build Failed"):
            sb.systems.execution.docker.build(config)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_run(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        job = config.jobs[0]
        job.mappings = ["data/", "/test/output/:/app/output/", "~/temp/:/app/temp/"]
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-build --rm -i -v $PWD/data/:/app/data/ -v /test/output/:/app/output/ -v {homePath}/temp/:/app/temp/ test /bin/bash -c './build.sh 0.1 --env local --log info'".format(homePath=homePath)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name)
        mock_system.assert_called_once_with(expected)

if __name__ == '__main__':
    unittest.main()
