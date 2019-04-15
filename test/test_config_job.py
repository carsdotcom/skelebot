from unittest import TestCase
import skelebot as sb

class TestConfigJob(TestCase):

    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        args   = [sb.config.Param("env", None, "local", ["local", "dev", "prod"])]
        params = [sb.config.Param("mode", "m", "local", ["local", "dev", "prod"])]
        yaml = sb.config.Job("run", "run.sh", "run the job", args, params, ["one", "two", "three"], "i").getYaml()
        expected = """name: run
source: run.sh
mode: i
help: run the job
args: 
- name: env
  default: local
  choices: 
  - local
  - dev
  - prod
params: 
- name: mode
  alt: m
  default: local
  choices: 
  - local
  - dev
  - prod
ignore: 
- one
- two
- three
"""
        self.assertEqual(expected, yaml)

    # Test that the YAML is built correctly with all params
    def test_getYamlRequired(self):
        yaml = sb.config.Job("run", "run.sh", "run the job").getYaml()
        expected = """name: run
source: run.sh
mode: i
help: run the job
"""
        self.assertEqual(expected, yaml)

if __name__ == '__main__':
    unittest.main()
