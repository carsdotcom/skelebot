import os
import unittest
from unittest import mock
from argparse import Namespace

import skelebot as sb

# Test plugin that says 'Hi' at the end of every command
class LimitMemory(sb.objects.component.Component):
    activation = sb.objects.component.Activation.CONFIG

    def __init__(self, memory):
        self.memory = memory

    def addDockerRunParams(self):
        return "--memory {memory}GB".format(memory=self.memory)

class TestDocker(unittest.TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.system')
    def test_login(self, mock_system):
        mock_system.return_value = 0

        sb.systems.execution.docker.login()
        mock_system.assert_called_once_with("docker login ")

    @mock.patch('os.system')
    def test_login_host(self, mock_system):
        mock_system.return_value = 0

        sb.systems.execution.docker.login("docker.io")
        mock_system.assert_called_once_with("docker login docker.io")

    @mock.patch('os.system')
    def test_login_error(self, mock_system):
        mock_system.return_value = 1

        with self.assertRaisesRegex(Exception, "Docker Login Failed"):
            sb.systems.execution.docker.login()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_push(self, mock_getcwd, mock_system, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        sb.systems.execution.docker.push(config, host, port, user)

        mock_system.assert_any_call("docker tag test docker.io:8888/skelebot/test:6.6.6")
        mock_system.assert_any_call("docker tag test docker.io:8888/skelebot/test:latest")
        mock_system.assert_any_call("docker push docker.io:8888/skelebot/test:6.6.6")
        mock_system.assert_any_call("docker push docker.io:8888/skelebot/test:latest")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_push_error(self, mock_getcwd, mock_system, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()

        with self.assertRaisesRegex(Exception, "Docker Push Failed"):
            sb.systems.execution.docker.push(config, host, port, user)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.remove')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_ephemeral(self, mock_getcwd, mock_system, mock_remove, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

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

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test .")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_with_env(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.env = 'test'

        sb.systems.execution.docker.build(config)
        mock_system.assert_called_once_with("docker build -t test-test .")

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_build_error(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

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
        config.ports = ["1127:1127"]
        job = config.jobs[0]
        job.mappings = ["data/", "/test/output/:/app/output/", "~/temp/:/app/temp/"]
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-build --rm -i -p 1127:1127 -v {cwd}/data/:/app/data/ -v /test/output/:/app/output/ -v {path}/temp/:/app/temp/ test /bin/bash -c \"bash build.sh 0.1 --env local --log info\"".format(cwd=folderPath, path=homePath)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name)
        mock_system.assert_called_once_with(expected)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.system')
    @mock.patch('os.getcwd')
    def test_run_docker_params(self, mock_getcwd, mock_system, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        memory = 256
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_system.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.components.append(LimitMemory(memory))
        job = sb.objects.job.Job(name='some_command', help='Dummy', source='echo some_command')
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-some_command --rm -i --memory {memory}GB test /bin/bash -c \"echo some_command\"".format(memory=memory)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name)
        mock_system.assert_called_once_with(expected)

    @mock.patch('os.system')
    def test_save(self, mock_system):
        mock_system.return_value = 0

        sb.systems.execution.docker.save(sb.objects.config.Config(name="Test Project"), "test.img")
        mock_system.assert_called_once_with("docker save -o test.img test-project")

if __name__ == '__main__':
    unittest.main()
