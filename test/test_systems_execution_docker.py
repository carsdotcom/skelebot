import os
import unittest
from unittest import mock
from argparse import Namespace

from colorama import Fore, Style

import skelebot as sb

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

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login(self, mock_call):
        mock_call.return_value = 0
        mock_call.configure_mock(shell=True)

        sb.systems.execution.docker.login()
        mock_call.assert_called_once_with("docker login ", shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_host(self, mock_call):
        mock_call.return_value = 0

        sb.systems.execution.docker.login("docker.io")
        mock_call.assert_called_once_with("docker login docker.io", shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_error(self, mock_call):
        mock_call.return_value = 1

        with self.assertRaisesRegex(Exception, "Docker Login Failed"):
            sb.systems.execution.docker.login()

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_aws_v2(self, mock_call):
        mock_call.return_value = 0

        sb.systems.execution.docker.loginAWS("123.dkr.ecr.us-east-1.amazonaws.com", "us-east-1", "dev")
        mock_call.assert_called_once_with("aws ecr get-login-password --region us-east-1 --profile dev | docker login --username AWS --password-stdin 123.dkr.ecr.us-east-1.amazonaws.com", shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_aws_v2_host(self, mock_call):
        mock_call.return_value = 0

        sb.systems.execution.docker.loginAWS("123.dkr.ecr.us-east-1.amazonaws.com", "us-east-1", "dev", "host1")
        mock_call.assert_called_once_with("aws ecr get-login-password --region us-east-1 --profile dev | docker -H host1 login --username AWS --password-stdin 123.dkr.ecr.us-east-1.amazonaws.com", shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_aws_v1(self, mock_call):
        mock_call.return_value = 1

        with self.assertRaisesRegex(Exception, "Docker Login V1 Failed"):
            sb.systems.execution.docker.loginAWS(None, "us-east-1", "dev")

        mock_call.return_value = 0

        sb.systems.execution.docker.loginAWS("123.dkr.ecr.us-east-1.amazonaws.com", "us-east-1", "dev")
        mock_call.assert_any_call("$(aws ecr get-login --no-include-email --region us-east-1 --profile dev)", shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_aws_v1_host(self, mock_call):
        mock_call.return_value = 1

        with self.assertRaisesRegex(Exception, "Docker Login V1 Failed"):
            sb.systems.execution.docker.loginAWS(None, "us-east-1", "dev")

        with self.assertRaisesRegex(Exception, "Remote hosts are not supported"):
            sb.systems.execution.docker.loginAWS(
                "123.dkr.ecr.us-east-1.amazonaws.com", "us-east-1", "dev", "host1"
            )

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_login_aws_error(self, mock_call):
        mock_call.return_value = 1

        with self.assertRaisesRegex(Exception, r"Docker Login .* Failed"):
            sb.systems.execution.docker.loginAWS(None, "us-east-1", "dev")

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_push(self, mock_getcwd, mock_call, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        sb.systems.execution.docker.push(config, host, port, user)

        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:latest", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:latest", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_push_host(self, mock_getcwd, mock_call, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        sb.systems.execution.docker.push(config, host, port, user, docker_host='host1')

        mock_call.assert_any_call("docker -H host1 tag test docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker -H host1 tag test docker.io:8888/skelebot/test:latest", shell=True)
        mock_call.assert_any_call("docker -H host1 push docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker -H host1 push docker.io:8888/skelebot/test:latest", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_push_tags(self, mock_getcwd, mock_call, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        sb.systems.execution.docker.push(config, host, port, user, tags=["DEV", "STG"])

        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:6.6.6", shell=True)
        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:latest", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:latest", shell=True)
        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:DEV", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:DEV", shell=True)
        mock_call.assert_any_call("docker tag test docker.io:8888/skelebot/test:STG", shell=True)
        mock_call.assert_any_call("docker push docker.io:8888/skelebot/test:STG", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_push_error(self, mock_getcwd, mock_call, mock_expanduser):
        host = "docker.io"
        port = 8888
        user = "skelebot"
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()

        with self.assertRaisesRegex(Exception, "Docker Command Failed"):
            sb.systems.execution.docker.push(config, host, port, user)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.remove')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_build_ephemeral(self, mock_getcwd, mock_call, mock_remove, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.ephemeral = True

        sb.systems.execution.docker.build(config, None)
        mock_call.assert_called_once_with("docker build -t test .", shell=True)
        mock_remove.assert_any_call("Dockerfile")
        mock_remove.assert_any_call(".dockerignore")

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_build_non_ephemeral(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.execution.docker.build(config, None)
        mock_call.assert_called_once_with("docker build -t test .", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_build_host(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.execution.docker.build(config, "root@hosty.McHostface")
        mock_call.assert_called_once_with("docker -H root@hosty.McHostface build -t test .", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_build_with_env(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.env = 'test'

        sb.systems.execution.docker.build(config, None)
        mock_call.assert_called_once_with("docker build -t test-test .", shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_build_error(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 1

        config = sb.systems.generators.yaml.loadConfig()

        with self.assertRaisesRegex(Exception, "Docker Build Failed"):
            sb.systems.execution.docker.build(config, None)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_run(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.ports = ["1127:1127"]
        job = config.jobs[0]
        job.mappings = ["data/", "/test/output/:/app/output/", "~/temp/:/app/temp/"]
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-build --rm -i -p 1127:1127 -v {cwd}/data/:/app/data/ -v /test/output/:/app/output/ -v {path}/temp/:/app/temp/ test /bin/bash -c \"bash build.sh 0.1 --env local --log info\"".format(cwd=folderPath, path=homePath)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name, host=None)
        mock_call.assert_called_once_with(expected, shell=True)
    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')

    def test_run_host(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.ports = ["1127:1127"]
        job = config.jobs[0]
        job.mappings = ["data/", "/test/output/:/app/output/", "~/temp/:/app/temp/"]
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker -H root@Hosty.McHostface run --name test-build --rm -i -p 1127:1127 -v {cwd}/data/:/app/data/ -v /test/output/:/app/output/ -v {path}/temp/:/app/temp/ test /bin/bash -c \"bash build.sh 0.1 --env local --log info\"".format(cwd=folderPath, path=homePath)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name, host="root@Hosty.McHostface")
        mock_call.assert_called_once_with(expected, shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_run_docker_params(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        memory = 256
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.components.append(LimitMemory(memory))
        job = sb.objects.job.Job(name='some_command', help='Dummy', source='echo some_command')
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-some_command --rm -i --memory {memory}GB test /bin/bash -c \"echo some_command\"".format(memory=memory)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name, host=None)
        mock_call.assert_called_once_with(expected, shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_run_docker_params_entrypoint(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        memory = 256
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.primaryExe = "ENTRYPOINT"
        config.components.append(LimitMemory(memory))
        job = sb.objects.job.Job(name='some_command', help='Dummy', source='echo some_command')
        command = sb.systems.execution.commandBuilder.build(config, job, args)

        expected = "docker run --name test-some_command --rm -i --memory {memory}GB --entrypoint echo test some_command".format(memory=memory)
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name, host=None)
        mock_call.assert_called_once_with(expected, shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('skelebot.systems.execution.docker.call')
    @mock.patch('os.getcwd')
    def test_run_gpu(self, mock_getcwd, mock_call, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        args = Namespace(version='0.1')

        homePath = "{path}/test/plugins".format(path=self.path)
        mock_expanduser.return_value = homePath
        mock_getcwd.return_value = folderPath
        mock_call.return_value = 0

        config = sb.systems.generators.yaml.loadConfig()
        config.gpu = True
        job = sb.objects.job.Job(name='some_command', help='Dummy', source='echo some_command')
        command = sb.systems.execution.commandBuilder.build(config, job, args)
        
        expected = "docker run --name test-some_command --rm -i --gpus all --ipc=host test /bin/bash -c \"echo some_command\""
        sb.systems.execution.docker.run(config, command, job.mode, config.ports, job.mappings, job.name, host=None)
        mock_call.assert_called_once_with(expected, shell=True)

    @mock.patch('skelebot.systems.execution.docker.call')
    def test_save(self, mock_call):
        mock_call.return_value = 0

        sb.systems.execution.docker.save(sb.objects.config.Config(name="Test Project"), "test.img")
        mock_call.assert_called_once_with("docker save -o test.img test-project", shell=True)

    @mock.patch('skelebot.systems.execution.docker.print')
    @mock.patch('skelebot.systems.execution.docker.call')
    def test_execute_verbose(self, mock_call, mock_print):
        mock_call.return_value = 0

        sb.systems.execution.docker.execute("echo foo", err_msg="Something bad", verbose=True)
        mock_print.assert_called_once_with(Fore.GREEN + "INFO" + Style.RESET_ALL + " | echo foo")
        mock_call.assert_called_once_with("echo foo", shell=True)

if __name__ == '__main__':
    unittest.main()
