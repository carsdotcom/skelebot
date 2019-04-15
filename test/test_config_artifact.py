from unittest import TestCase
import skelebot as sb

class TestConfigArtifact(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        deploy = [sb.config.Deploy("Artifactory", "repo.cars.com", "cml", "my-ds-proj")]
        yaml = sb.config.Artifact("model", "mymodel.RData", deploy).getYaml()
        expected = """name: model
file: mymodel.RData
deploy: 
- type: Artifactory
  url: repo.cars.com
  repo: cml
  path: my-ds-proj
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
