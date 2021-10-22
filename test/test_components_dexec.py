import argparse
import unittest
from unittest import mock

import skelebot as sb

class TestDexec(unittest.TestCase):

    def test_addParsers(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        dexec = sb.components.dexec.Dexec()
        subparsers = dexec.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["exec"], None)

    @mock.patch('skelebot.components.dexec.docker')
    def test_execute_nomap(self, mock_docker):
        config = sb.objects.config.Config(name="test-dexec")
        args = argparse.Namespace(map=False, verbose_global=False)

        dexec = sb.components.dexec.Dexec()
        dexec.execute(config, args)

        mock_docker.build.assert_called_with(config, host=None, verbose=False)
        mock_docker.run.assert_called_with(
            config, "/bin/bash", "it", [], [], "exec", host=None, verbose=False
        )

    @mock.patch('skelebot.components.dexec.docker')
    def test_execute_map(self, mock_docker):
        config = sb.objects.config.Config(name="test-dexec")
        args = argparse.Namespace(map=True, verbose_global=False)

        dexec = sb.components.dexec.Dexec()
        dexec.execute(config, args)

        mock_docker.build.assert_called_with(config, host=None, verbose=False)
        mock_docker.run.assert_called_with(
            config, "/bin/bash", "it", [], ["."], "exec", host=None, verbose=False
        )

if __name__ == '__main__':
    unittest.main()
