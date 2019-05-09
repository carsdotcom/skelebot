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

    # Test to ensure that the config loads from skelebot.yaml properly when it is present
    @mock.patch('os.getcwd')
    def test_loadConfig_with_yaml(self, mock_getcwd):
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)

        config = sb.files.yaml.loadConfig()
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
        # [TODO] Validate the jobs list of objects
        components = []
        for component in config.components:
            componentClass = component.__class__.__name__
            components.append(componentClass)
            self.assertNotEqual(component.activation, Activation.EMPTY)

            if (componentClass == "Jupyter"):
                self.assertEqual(component.port, 1127)
                self.assertEqual(component.folder, "notebooks/")

        expectedComponents = ["Plugin", "Jupyter"]
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

    # Test to ensure that the config loads the default values when no skelebot.yaml is present
    @mock.patch('os.getcwd')
    def test_loadConfig_without_yaml(self, mock_getcwd):
        mock_getcwd.return_value = "{path}/test".format(path=self.path)

        config = sb.files.yaml.loadConfig()

        components = []
        for component in config.components:
            components.append(component.__class__.__name__)
            self.assertEqual((component.activation == Activation.ALWAYS) or (component.activation == Activation.EMPTY), True)

        expectedComponents = ["Plugin"]
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

if __name__ == '__main__':
    unittest.main()
