from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os

class TestJupyter(TestCase):

    def test_addParsers(self):
        jupyter = sb.components.jupyter.Jupyter(port=1127, folder="notebooks/")

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = jupyter.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["jupyter"], None)

    @mock.patch('skelebot.components.jupyter.docker')
    def test_execute_R(self, mock_docker):
        mock_docker.build.return_value = 0
        config = sb.objects.config.Config(language="R")
        args = argparse.Namespace()

        jupyter = sb.components.jupyter.Jupyter(port=1127, folder="notebooks/")
        jupyter.execute(config, args)

        expectedCommand = "jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir=notebooks/"

        mock_docker.build.assert_called_with(config)
        mock_docker.run.assert_called_with(config, expectedCommand, "i", ["1127:8888"], ".", "jupyter")

    @mock.patch('skelebot.components.jupyter.docker')
    def test_execute_Python(self, mock_docker):
        mock_docker.build.return_value = 0
        config = sb.objects.config.Config(language="Python")
        args = argparse.Namespace()

        jupyter = sb.components.jupyter.Jupyter(port=1127, folder="notebooks/")
        jupyter.execute(config, args)

        expectedCommand = "jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --notebook-dir=notebooks/"

        mock_docker.build.assert_called_with(config)
        mock_docker.run.assert_called_with(config, expectedCommand, "i", ["1127:8888"], ".", "jupyter")

if __name__ == '__main__':
    unittest.main()
