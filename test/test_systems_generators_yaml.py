import os
import unittest
from unittest import mock
from colorama import Fore, Style

from skelebot.objects.component import Activation

import skelebot as sb

class TestYaml(unittest.TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()

    def validateYaml(self, config, isTestEnv=False):
        self.assertEqual(config.name, "test")
        self.assertEqual(config.description, "test cases")
        self.assertEqual(config.version, "6.6.6")
        self.assertEqual(config.maintainer, "Mega Man")
        self.assertEqual(config.contact, "megaman@cars.com")
        self.assertEqual(config.language, "Python")
        self.assertEqual(config.primaryJob, "build")
        self.assertEqual(config.ephemeral, True if isTestEnv else None)
        self.assertEqual(config.dependencies, ["pyyaml", "artifactory", "argparse", "coverage", "pytest"])
        if isTestEnv:
            self.assertEqual(config.ignores, ['data/', 'libs/'])
        else:
            self.assertEqual(config.ignores, ['**/*.zip', '**/*.RData', '**/*.pkl', '**/*.csv', '**/*.model', '**/*.pyc'])
        self.assertEqual(config.commands, ["rm -rf build/", "rm -rf dist/"])
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
                self.assertEqual(component.port, 1128 if isTestEnv else 1127)
                self.assertEqual(component.folder, "notebooks/")

        expectedComponents = ["Registry", "Plugin", "Jupyter", "Bump", "Prime", "Environments", "Dexec", "AddNumbers"]
        if not isTestEnv:
            expectedComponents.append("Artifactory")
        else:
            expectedComponents.append("Repository")
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

    # Test to ensure that the config loads from skelebot.yaml properly when it is present
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_loadConfig_with_yaml(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        config = sb.systems.generators.yaml.loadConfig()
        self.validateYaml(config)

    # Test to ensure that the config loads from skelebot.yaml properly even if a bad plugin is found and quarantined
    @mock.patch('skelebot.components.componentFactory.print')
    @mock.patch('shutil.move')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_loadConfig_with_bad_plugin(self, mock_getcwd, mock_expanduser, mock_exists, mock_makedirs, mock_shutil, mock_print):
        mock_expanduser.return_value = "{path}/test/plugins-bad".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        mock_exists.side_effect = [True, False]
        config = sb.systems.generators.yaml.loadConfig()

        folder = "{}/test/plugins-bad/addNumbersBad".format(self.path)
        mock_print.assert_called_with(Fore.YELLOW + "WARNING" + Style.RESET_ALL + " | The addNumbersBad plugin contains errors - Adding plugin to Quarantine")
        mock_makedirs.assert_called_with("{path}/test/plugins-bad".format(path=self.path))
        mock_shutil.assert_called_with(folder, folder)

    # Test to ensure that the config loads from skelebot.yaml and overwrites with skelebot-test.yaml properly
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_loadConfig_with_env(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        config = sb.systems.generators.yaml.loadConfig("test")
        self.validateYaml(config, True)

    # Test to ensure that the config loads from skelebot.yaml and overwrites with skelebot-test.yaml properly
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_loadConfig_with_env_not_found(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        try:
            sb.systems.generators.yaml.loadConfig("tests")
            self.fail("Exception Expected")
        except RuntimeError as error:
            self.assertEqual(str(error), "Environment Not Found")

    # Test to ensure that the config loads the default values when no skelebot.yaml is present
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_loadConfig_without_yaml(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test".format(path=self.path)

        config = sb.systems.generators.yaml.loadConfig()

        self.assertEqual(config.name, None)
        self.assertEqual(config.env, None)
        self.assertEqual(config.description, None)
        self.assertEqual(config.version, None)
        self.assertEqual(config.maintainer, None)
        self.assertEqual(config.contact, None)
        self.assertEqual(config.language, None)
        self.assertEqual(config.primaryJob, None)
        self.assertEqual(config.ephemeral, None)
        self.assertEqual(config.dependencies, [])
        self.assertEqual(config.ignores, [])
        self.assertEqual(config.commands, [])
        self.assertEqual(config.jobs, [])
        components = []
        for component in config.components:
            components.append(component.__class__.__name__)
            self.assertEqual((component.activation == Activation.ALWAYS) or (component.activation == Activation.EMPTY), True)

        expectedComponents = ["Plugin", "AddNumbers"]
        self.assertTrue(all(elem in components for elem in expectedComponents))
        self.assertTrue(all(elem in expectedComponents for elem in components))

    # Test to ensure that the yaml generation works properly with a complete config object (ends up testing the loading process as well)
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_saveConfig(self, mock_getcwd, mock_expanduser):
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = "{path}/test/files".format(path=self.path)
        config = sb.systems.generators.yaml.loadConfig()

        sb.systems.generators.yaml.saveConfig(config)
        config = sb.systems.generators.yaml.loadConfig()
        self.validateYaml(config)


if __name__ == '__main__':
    unittest.main()
