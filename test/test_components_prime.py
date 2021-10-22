import argparse
import unittest
from unittest import mock

import skelebot as sb

class TestPrime(unittest.TestCase):

    def test_addParsers(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="prime")
        prime = sb.components.prime.Prime()
        subparsers = prime.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["prime"], None)

    @mock.patch('skelebot.components.prime.docker')
    def test_execute(self, mock_docker):
        mock_docker.build.return_value = 0
        mock_docker.save.return_value = 0

        config = sb.objects.config.Config()
        args = argparse.Namespace(output=None, verbose_global=False)

        prime = sb.components.prime.Prime()
        prime.execute(config, args)

        mock_docker.build.assert_called_with(config, host=None, verbose=False)

    @mock.patch('skelebot.components.prime.docker')
    def test_execute_host(self, mock_docker):
        mock_docker.build.return_value = 0
        mock_docker.save.return_value = 0

        config = sb.objects.config.Config()
        args = argparse.Namespace(output=None, verbose_global=False)

        prime = sb.components.prime.Prime()
        prime.execute(config, args, host='host1')

        mock_docker.build.assert_called_with(config, host='host1', verbose=False)

    @mock.patch('skelebot.components.prime.docker')
    def test_execute_output(self, mock_docker):
        mock_docker.build.return_value = 0
        mock_docker.save.return_value = 0

        config = sb.objects.config.Config()
        args = argparse.Namespace(output="my-image.img", verbose_global=False)

        prime = sb.components.prime.Prime()
        prime.execute(config, args)

        mock_docker.build.assert_called_with(config, host=None, verbose=False)
        mock_docker.save.assert_called_with(config, "my-image.img", host=None, verbose=False)

    @mock.patch('skelebot.components.prime.docker')
    def test_execute_exception(self, mock_docker):
        mock_docker.build.return_value = 0
        mock_docker.save.return_value = 1

        config = sb.objects.config.Config()
        args = argparse.Namespace(output="my-image.img", verbose_global=False)

        prime = sb.components.prime.Prime()
        try:
            prime.execute(config, args)
            self.fail("Exception Expected")
        except Exception as exc:
            self.assertEqual(str(exc), "Priming Failed")
            mock_docker.build.assert_called_with(config, host=None, verbose=False)
            mock_docker.save.assert_called_with(config, "my-image.img", host=None, verbose=False)

if __name__ == '__main__':
    unittest.main()
