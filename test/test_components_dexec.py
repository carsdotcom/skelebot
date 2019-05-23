from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse

class TestDexec(TestCase):

    def test_addParsers(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        dexec = sb.components.dexec.Dexec()
        subparsers = dexec.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["exec"], None)

    @mock.patch('skelebot.components.dexec.docker')
    def test_execute(self, mock_docker):
        config = sb.objects.config.Config(name="test-dexec")
        args = argparse.Namespace()

        dexec = sb.components.dexec.Dexec()
        dexec.execute(config, args)

        mock_docker.build.assert_called_with(config)
        mock_docker.run.assert_called_with(config, "/bin/bash", "it", [], [], "test-dexec-exec")

if __name__ == '__main__':
    unittest.main()
