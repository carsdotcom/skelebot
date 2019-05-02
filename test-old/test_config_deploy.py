from unittest import TestCase
import skelebot as sb

class TestConfigDeploy(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        yaml = sb.config.Deploy("Artifactory", "repo.cars.com", "cml", "my-ds-proj").getYaml()
        expected = """type: Artifactory
url: repo.cars.com
repo: cml
path: my-ds-proj
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
