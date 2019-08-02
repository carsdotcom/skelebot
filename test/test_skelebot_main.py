from unittest import TestCase
from unittest import mock

import skelebot as sb

class TestSkelebotMain(TestCase):

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

        with mock.patch("sys.argv", ["main", "-e", "dev"]):
            sb.main()

        mock_yaml.assert_called_once_with("dev")
        mock_parser.assert_called_once_with("config", "dev")
        mock_executor.assert_called_once_with("config", "parser")
