import unittest
import os

import skelebot as sb

class TestDockerignore(unittest.TestCase):
    path = ""
    config = None

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @unittest.mock.patch('os.path.expanduser')
    @unittest.mock.patch('os.getcwd')
    def test_buildDockerignore(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/.dockerignore".format(folder=folderPath)
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        self.config = sb.systems.generators.yaml.loadConfig()

        expected = """
# This dockerignore was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

**/*.zip
**/*.RData
**/*.pkl
**/*.csv
**/*.model
**/*.pyc
"""

        sb.systems.generators.dockerignore.buildDockerignore(self.config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expected)

if __name__ == '__main__':
    unittest.main()
