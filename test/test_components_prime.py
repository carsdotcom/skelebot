from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse

class TestPrime(TestCase):

    def test_addParsers(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="prime")
        prime = sb.components.prime.Prime()
        subparsers = prime.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["prime"], None)

    @mock.patch('skelebot.components.prime.docker')
    def test_execute(self, mock_docker):
        config = sb.objects.config.Config()
        args = argparse.Namespace()

        prime = sb.components.prime.Prime()
        prime.execute(config, args)

        mock_docker.build.assert_called_with(config)

if __name__ == '__main__':
    unittest.main()
