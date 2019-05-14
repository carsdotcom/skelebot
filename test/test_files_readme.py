from unittest import TestCase
from unittest import mock

import skelebot as sb
import os

class TestREADME(TestCase):
    path = ""
    config = None

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.getcwd')
    def test_buildREADME(self, mock_getcwd):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/README.md".format(folder=folderPath)
        mock_getcwd.return_value = folderPath
        self.config = sb.files.yaml.loadConfig()

        expected= """# test
![Version](https://img.shields.io/badge/Version-6.6.6-brightgreen.svg)
![Documentation](https://img.shields.io/badge/Documentation-UNLINKED-red.svg)

test cases

---

## Contact
Project Maintainer: Mega Man (megaman@cars.com)"""


        sb.files.readme.buildREADME(self.config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expected)

if __name__ == '__main__':
    unittest.main()
