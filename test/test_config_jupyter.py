
from unittest import TestCase
import skelebot as sb

class TestConfigJupyter(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        yaml = sb.config.Jupyter(8080, "notebooks/").getYaml()
        expected = """port: 8080
folder: notebooks/
"""
        self.assertEqual(expected, yaml)

    # Test that the YAML is built correctly with all params
    def test_getYamlDefaults(self):
        yaml = sb.config.Jupyter().getYaml()
        expected = """port: 8888
folder: .
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
