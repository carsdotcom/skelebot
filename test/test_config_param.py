from unittest import TestCase
import skelebot as sb

class TestConfigParam(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        yaml = sb.config.Param("env", "e", "local", ["local", "dev", "prod"]).getYaml()
        expected = "name: env\nalt: e\ndefault: local\nchoices: \n- local\n- dev\n- prod\n"
        self.assertEqual(expected, yaml)

    # Test that the YAML is built correctly with only required params
    def test_getYamlRequired(self):
        yaml = sb.config.Param("env", "e").getYaml()
        expected = "name: env\nalt: e\n"
        self.assertEqual(expected, yaml)

    # Test that the YAML is built correctly with choices
    def test_getYamlChoices(self):
        yaml = sb.config.Param("env", "e", choices=["local", "dev", "prod"]).getYaml()
        expected = "name: env\nalt: e\nchoices: \n- local\n- dev\n- prod\n"
        self.assertEqual(expected, yaml)

    # Test that the YAML is built correctly with default
    def test_getYamlDefault(self):
        yaml = sb.config.Param("env", "e", "local").getYaml()
        expected = "name: env\nalt: e\ndefault: local\n"
        self.assertEqual(expected, yaml)


if __name__ == '__main__':
    unittest.main()
