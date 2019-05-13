from unittest import TestCase
from unittest import mock

import skelebot as sb
import os

class TestDockerfile(TestCase):
    path = ""
    config = None

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.getcwd')
    def test_buildDokcerfile(self, mock_getcwd):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)
        mock_getcwd.return_value = folderPath
        self.config = sb.files.yaml.loadConfig()

        sb.files.dockerfile.buildDockerfile(self.config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        # [TODO] Verify the contents of the Dockerfile

if __name__ == '__main__':
    unittest.main()
