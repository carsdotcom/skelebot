import os
import unittest
from unittest import mock

import skelebot as sb

class TestREADME(unittest.TestCase):
    path = ""
    config = None

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildREADME(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/README.md".format(folder=folderPath)
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        self.config = sb.systems.generators.yaml.loadConfig()

        expected = """# test
![Version](https://img.shields.io/badge/Version-6.6.6-brightgreen.svg)
![Documentation](https://img.shields.io/badge/Documentation-UNLINKED-red.svg)

test cases

---

## Contact
Project Maintainer: Mega Man (megaman@cars.com)"""


        sb.systems.generators.readme.buildREADME(self.config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expected)

if __name__ == '__main__':
    unittest.main()
