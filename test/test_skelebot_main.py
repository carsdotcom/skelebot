import unittest
from unittest import mock

from schema import SchemaError
from colorama import Fore, Style

import skelebot as sb

class TestSkelebotMain(unittest.TestCase):

    @mock.patch('skelebot.systems.execution.executor.execute')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    @mock.patch('skelebot.systems.parsing.skeleParser.SkeleParser')
    def test_skelebot_main(self, mock_parser, mock_yaml, mock_executor):
        mock_parser.return_value = "parser"
        mock_yaml.return_value = "config"
        mock_executor.return_value = 0

        sb.main()

        mock_yaml.assert_called_once_with(None)
        mock_parser.assert_called_once_with("config", None)
        mock_executor.assert_called_once_with("config", "parser")

    @mock.patch('skelebot.systems.execution.executor.execute')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    @mock.patch('skelebot.systems.parsing.skeleParser.SkeleParser')
    def test_skelebot_main_env(self, mock_parser, mock_yaml, mock_executor):
        mock_parser.return_value = "parser"
        mock_yaml.return_value = "config"
        mock_executor.return_value = 0

        with mock.patch("sys.argv", ["path/to/skelebot", "-e", "dev"]):
            sb.main()

        mock_yaml.assert_called_once_with("dev")
        mock_parser.assert_called_once_with("config", "dev")
        mock_executor.assert_called_once_with("config", "parser")

    @mock.patch('skelebot.systems.execution.executor.execute')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    @mock.patch('skelebot.systems.parsing.skeleParser.SkeleParser')
    def test_skelebot_main_job_env(self, mock_parser, mock_yaml, mock_executor):
        mock_parser.return_value = "parser"
        mock_yaml.return_value = "config"
        mock_executor.return_value = 0

        with mock.patch("sys.argv", ["skelebot", "train", "-e", "dev"]):
            sb.main()

        mock_yaml.assert_called_once_with(None)
        mock_parser.assert_called_once_with("config", None)
        mock_executor.assert_called_once_with("config", "parser")

    @mock.patch('skelebot.systems.execution.executor.execute')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    @mock.patch('skelebot.systems.parsing.skeleParser.SkeleParser')
    def test_skelebot_main_job_env(self, mock_parser, mock_yaml, mock_executor):
        mock_parser.return_value = "parser"
        mock_yaml.return_value = "config"
        mock_executor.return_value = 0

        with mock.patch("sys.argv", ["skelebot", "-s", "-n", "train", "-e", "dev"]):
            sb.main()

        mock_yaml.assert_called_once_with(None)
        mock_parser.assert_called_once_with("config", None)
        mock_executor.assert_called_once_with("config", "parser")

    @mock.patch('builtins.print')
    @mock.patch('sys.exit')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    def test_skelebot_schema_error(self, mock_yaml, exit_mock, print_mock):
        mock_yaml.side_effect = SchemaError("Validation Failed")

        sb.main()

        print_mock.assert_called_once_with(Fore.RED + "ERROR" + Style.RESET_ALL + " | skelebot.yaml | Validation Failed")
        exit_mock.assert_called_once_with(1)

    @mock.patch('builtins.print')
    @mock.patch('sys.exit')
    @mock.patch('skelebot.systems.generators.yaml.loadConfig')
    def test_skelebot_runtime_error(self, mock_yaml, exit_mock, print_mock):
        mock_yaml.side_effect = RuntimeError("Environment Not Found")

        sb.main()

        print_mock.assert_called_once_with(Fore.RED + "ERROR" + Style.RESET_ALL + " | Environment Not Found")
        exit_mock.assert_called_once_with(1)
