import argparse
import unittest
from unittest import mock

import skelebot as sb

class TestExecutor(unittest.TestCase):

    @mock.patch('skelebot.systems.execution.executor.print')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    @mock.patch('skelebot.systems.execution.executor.VERSION', '6.6.6')
    def test_execute_version(self, mock_skeleParser, mock_print):
        config = sb.objects.config.Config()
        args = argparse.Namespace(job=None, version_global=True)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_print.assert_called_with("Skelebot v6.6.6")

    @mock.patch('skelebot.systems.execution.executor.print')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_contact(self, mock_skeleParser, mock_print):
        config = sb.objects.config.Config(contact="me@my-mail.com")
        args = argparse.Namespace(job=None, contact_global=True)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_print.assert_called_with("me@my-mail.com")

    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_help(self, mock_skeleParser):
        config = sb.objects.config.Config()
        args = argparse.Namespace(job=None)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_skeleParser.showHelp.assert_called_once()

    @mock.patch('skelebot.systems.execution.executor.scaffold')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_scaffold(self, mock_skeleParser, mock_scaffold):
        config = sb.objects.config.Config()
        args = argparse.Namespace(job="scaffold", existing=False)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_scaffold.assert_called_once_with(False)

    @mock.patch('skelebot.systems.execution.executor.runDocker')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_job_skip(self, mock_skeleParser, mock_run):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native_global=False, skip_build_global=True)
        mock_skeleParser.parseArgs.return_value = args
        mock_run.return_value = 0

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_run.assert_called_once_with(config, "python -u test.py", "i", [], [], "test")

    @mock.patch('skelebot.systems.execution.executor.buildDocker')
    @mock.patch('skelebot.systems.execution.executor.runDocker')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_job(self, mock_skeleParser, mock_run, mock_build):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native_global=False, skip_build_global=False)
        mock_skeleParser.parseArgs.return_value = args
        mock_run.return_value = 0

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_build.assert_called_once_with(config)
        mock_run.assert_called_once_with(config, "python -u test.py", "i", [], [], "test")

    @mock.patch('os.system')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_job_native(self, mock_skeleParser, mock_system):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native_global=True)
        mock_skeleParser.parseArgs.return_value = args
        mock_system.return_value = 0

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_system.assert_called_once_with("python -u test.py")

    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_component(self, mock_skeleParser):
        mock_component = mock.MagicMock()
        mock_component.commands = ["test"]
        config = sb.objects.config.Config(components=[mock_component])
        args = argparse.Namespace(job="test")
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_component.execute.assert_called_once_with(config, args)

    @mock.patch('skelebot.systems.execution.executor.runDocker')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_chain(self, mock_skeleParser, mock_run):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native_global=False, skip_build_global=True)
        mock_skeleParser.parseArgs.return_value = args
        mock_run.return_value = 0

        sb.systems.execution.executor.execute(config, mock_skeleParser, ["test", "+", "test"])

        test_call = mock.call(config, "python -u test.py", "i", [], [], "test")
        mock_run.assert_has_calls([test_call, test_call])

    @mock.patch('skelebot.systems.execution.executor.runDocker')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_chain_fail(self, mock_skeleParser, mock_run):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native_global=False, skip_build_global=True)
        mock_skeleParser.parseArgs.return_value = args
        mock_run.return_value = 1
        try:
            sb.systems.execution.executor.execute(config, mock_skeleParser, ["test", "+", "test"])
            self.fail('exception expected')
        except SystemExit:
            mock_run.assert_called_once_with(config, "python -u test.py", "i", [], [], "test")

if __name__ == '__main__':
    unittest.main()
