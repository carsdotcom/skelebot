from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os

class TestPlugin(TestCase):

    def test_addParsers(self):
        plugin = sb.components.plugin.Plugin()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = plugin.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["plugin"], None)

    @mock.patch('skelebot.components.plugin.zipfile')
    def test_execute(self, mock_zipfile):
        mock_zip = mock.MagicMock()
        mock_zipfile.ZipFile.return_value = mock_zip
        config = sb.objects.config.Config()
        args = argparse.Namespace(plugin="test.zip")

        plugin = sb.components.plugin.Plugin()
        plugin.execute(config, args)

        mock_zipfile.ZipFile.assert_called_with("test.zip", "r")
        mock_zip.extractall.assert_called()
        mock_zip.close.assert_called()

if __name__ == '__main__':
    unittest.main()
