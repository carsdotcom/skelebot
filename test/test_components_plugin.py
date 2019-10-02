import argparse
import unittest
from unittest import mock

import skelebot as sb

class TestPlugin(unittest.TestCase):

    def test_addParsers(self):
        plugin = sb.components.plugin.Plugin()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = plugin.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["plugin"], None)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.components.plugin.zipfile')
    def test_execute(self, mock_zipfile, mock_makedirs, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/dummy"
        mock_exists.return_value = False

        mock_zip = mock.MagicMock()
        mock_zipfile.ZipFile.return_value = mock_zip
        config = sb.objects.config.Config()
        args = argparse.Namespace(plugin="test.zip")

        plugin = sb.components.plugin.Plugin()
        plugin.execute(config, args)

        mock_zipfile.ZipFile.assert_called_with("test.zip", "r")
        mock_zip.extractall.assert_called()
        mock_zip.close.assert_called()

        mock_makedirs.assert_any_call("test/dummy", exist_ok=True)

if __name__ == '__main__':
    unittest.main()
