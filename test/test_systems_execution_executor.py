from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse

class TestExecutor(TestCase):

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
        args = argparse.Namespace(job="test", native=False, skip_build=True)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_run.assert_called_once_with(config, "python -u test.py", "i", [], [], "test")

    @mock.patch('skelebot.systems.execution.executor.buildDocker')
    @mock.patch('skelebot.systems.execution.executor.runDocker')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_job(self, mock_skeleParser, mock_run, mock_build):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native=False, skip_build=False)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser)

        mock_build.assert_called_once_with(config)
        mock_run.assert_called_once_with(config, "python -u test.py", "i", [], [], "test")

    @mock.patch('os.system')
    @mock.patch('skelebot.systems.parsing.skeleParser')
    def test_execute_job_native(self, mock_skeleParser, mock_system):
        job = sb.objects.job.Job(name="test", source="test.py")
        config = sb.objects.config.Config(jobs=[job])
        args = argparse.Namespace(job="test", native=True)
        mock_skeleParser.parseArgs.return_value = args

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
        args = argparse.Namespace(job="test", native=False, skip_build=True)
        mock_skeleParser.parseArgs.return_value = args

        sb.systems.execution.executor.execute(config, mock_skeleParser, ["test", "+", "test"])

        mock_run.assert_called_with(config, "python -u test.py", "i", [], [], "test")

if __name__ == '__main__':
    unittest.main()
