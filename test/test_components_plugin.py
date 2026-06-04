import argparse
import os
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

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.components.plugin.zipfile.ZipFile')
    def test_execute(self, mock_zipfile, mock_makedirs, mock_exists, mock_expanduser, mock_open):
        mock_expanduser.return_value = "test/dummy"
        mock_exists.return_value = False
        pluginsRoot = os.path.realpath("test/dummy")

        mock_plugin_dir = mock.MagicMock()
        mock_plugin_dir.filename = "some_plug/"
        mock_plugin_dir.is_dir.return_value = True

        mock_plugin_script = mock.MagicMock()
        mock_plugin_script.filename = "some_plug/some_plug.py"
        mock_plugin_script.is_dir.return_value = False

        mock_zip_ref = mock.MagicMock()
        mock_zip_ref.infolist.return_value = [mock_plugin_dir, mock_plugin_script]
        mock_zipfile.return_value.__enter__.return_value = mock_zip_ref
        config = sb.objects.config.Config()
        args = argparse.Namespace(plugin="test.zip")

        plugin = sb.components.plugin.Plugin()
        plugin.execute(config, args)

        mock_zipfile.assert_called_once_with("test.zip", "r")
        mock_makedirs.assert_any_call("test/dummy", exist_ok=True)
        mock_makedirs.assert_any_call(os.path.join(pluginsRoot, "some_plug"), exist_ok=True)
        mock_zip_ref.open.assert_called_once_with(mock_plugin_script)
        mock_open.assert_called_once_with(
            os.path.join(pluginsRoot, "some_plug", "some_plug.py"), "wb"
        )


    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.components.plugin.zipfile.ZipFile')
    def test_execute_rejects_path_traversal(self, mock_zipfile, mock_makedirs, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/dummy"
        mock_exists.return_value = True

        evil = mock.MagicMock()
        evil.filename = "../../etc/passwd"
        evil.is_dir.return_value = False

        mock_zip_ref = mock.MagicMock()
        mock_zip_ref.infolist.return_value = [evil]
        mock_zipfile.return_value.__enter__.return_value = mock_zip_ref

        config = sb.objects.config.Config()
        args = argparse.Namespace(plugin="evil.zip")

        plugin = sb.components.plugin.Plugin()
        with self.assertRaises(RuntimeError):
            plugin.execute(config, args)

if __name__ == '__main__':
    unittest.main()
