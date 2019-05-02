from unittest import TestCase
import skelebot as sb

class TestConfigPlugin(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        cfgData = {'one': '1', 'two': '2'}
        yaml = sb.config.Plugin("blorb", cfgData).getYaml()
        expected = """name: blorb
config: 
  one: 1
  two: 2
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
