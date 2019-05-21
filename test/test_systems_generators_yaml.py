from unittest import TestCase
from unittest import mock
from skelebot.objects.component import Activation
import skelebot as sb
import os

class TestYaml(TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    def validateYaml(self, config):
        self.assertEqual(config.name, "test")
        self.assertEqual(config.description, "test cases")
        self.assertEqual(config.version, "6.6.6")
        self.assertEqual(config.skelebotVersion, "0.1.0")
        self.assertEqual(config.maintainer, "Mega Man")
        self.assertEqual(config.contact, "megaman@cars.com")
        self.assertEqual(config.language, "Python")
        self.assertEqual(config.primaryJob, "build")
        self.assertEqual(config.ephemeral, False)
        self.assertEqual(config.dependencies, ["pyyaml", "artifactory", "argparse", "coverage", "pytest"])
        self.assertEqual(config.ignores, ['**/*.zip', '**/*.RData', '**/*.pkl', '**/*.csv', '**/*.model', '**/*.pyc'])
        self.assertEqual(config.jobs[0].name, "build")
        self.assertEqual(config.jobs[0].source, "build.sh")
        self.assertEqual(config.jobs[0].mode, "i")
        self.assertEqual(config.jobs[0].help, "Build")
        self.assertEqual(config.jobs[0].mappings, ["data/", "output/", "temp/"])
        self.assertEqual(config.jobs[0].ignores, ["data/bigFile.pkl", "data/evenBiggerFile.pkl"])
        self.assertEqual(config.jobs[0].args[0].name, "version")
        self.assertEqual(config.jobs[0].params[0].name, "env")
        self.assertEqual(config.jobs[0].params[0].alt, "e")
        self.assertEqual(config.jobs[0].params[0].default, "local")
        self.assertEqual(config.jobs[0].params[0].choices, ["local", "dev", "prod"])
        components = []
        for component in config.components:
            componentClass = component.__class__.__name__
            components.append(componentClass)
            self.assertNotEqual(component.activation, Activation.EMPTY)

            if (componentClass == "Jupyter"):
                self.assertEqual(component.port, 1127)
                self.assertEqual(component.folder, "notebooks/")

        expectedComponents = ["Plugin", "Jupyter", "Bump", "Prime", "Dexec"]
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

    # Test to ensure that the config loads from skelebot.yaml properly when it is present
    @mock.patch('os.getcwd')
    def test_loadConfig_with_yaml(self, mock_getcwd):
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        config = sb.systems.generators.yaml.loadConfig()
        self.validateYaml(config)

    # Test to ensure that the config loads the default values when no skelebot.yaml is present
    @mock.patch('os.getcwd')
    def test_loadConfig_without_yaml(self, mock_getcwd):
        mock_getcwd.return_value = "{path}/test".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()

        self.assertEqual(config.name, None)
        self.assertEqual(config.description, None)
        self.assertEqual(config.version, None)
        self.assertEqual(config.skelebotVersion, None)
        self.assertEqual(config.maintainer, None)
        self.assertEqual(config.contact, None)
        self.assertEqual(config.language, None)
        self.assertEqual(config.primaryJob, None)
        self.assertEqual(config.ephemeral, None)
        self.assertEqual(config.dependencies, [])
        self.assertEqual(config.ignores, [])
        self.assertEqual(config.jobs, [])
        components = []
        for component in config.components:
            components.append(component.__class__.__name__)
            self.assertEqual((component.activation == Activation.ALWAYS) or (component.activation == Activation.EMPTY), True)

        expectedComponents = ["Plugin"]
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

    # Test to ensure that the yaml generation works properly with a complete config object (ends up testing the loading process as well)
    @mock.patch('os.getcwd')
    def test_saveConfig(self, mock_getcwd):
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.generators.yaml.saveConfig(config)
        config = sb.systems.generators.yaml.loadConfig()
        self.validateYaml(config)


if __name__ == '__main__':
    unittest.main()
