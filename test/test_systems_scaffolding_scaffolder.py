import os
import unittest
from unittest import mock

import skelebot as sb

class TestScaffolder(unittest.TestCase):

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_abort(self, mock_prompt, mock_cFactory, mock_getcwd, mock_exists,
                                    mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_exists.return_value = False
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", "Default", False]
        try:
            scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
            scaffolder.scaffold()
            self.fail("Exception Expected")
        except Exception as exc:
            self.assertEqual(str(exc), "Aborting Scaffolding Process")

            mock_prompt.assert_any_call("Enter a PROJECT NAME")
            mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
            mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
            mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
            mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
            mock_prompt.assert_any_call("Select a TEMPLATE", options=["Dash", "Package", "Default"])
            mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    #@mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_existing_init(self, mock_prompt, mock_yaml, #mock_cFactory,
                                            mock_makedirs, mock_getcwd, mock_exists,
                                            mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_exists.return_value = False
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", "Dash", True]

        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=True)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Select a TEMPLATE", options=["Dash", "Package", "Default"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.Config')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerfile')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerignore')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.readme')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_container_r(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_makedirs,
                              mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "R", "Default", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.load.assert_called_once()

        mock_makedirs.assert_any_call("config/", exist_ok=True)
        mock_makedirs.assert_any_call("data/", exist_ok=True)
        mock_makedirs.assert_any_call("queries/", exist_ok=True)
        mock_makedirs.assert_any_call("src/jobs/", exist_ok=True)

        mock_dockerfile.buildDockerfile.assert_called_once()
        mock_dignore.buildDockerignore.assert_called_once()
        mock_readme.buildREADME.assert_called_once()
        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.Config')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerfile')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerignore')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.readme')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_container_r_python(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_makedirs,
                              mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "R+Python", "Default", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.load.assert_called_once()

        mock_makedirs.assert_any_call("config/", exist_ok=True)
        mock_makedirs.assert_any_call("data/", exist_ok=True)
        mock_makedirs.assert_any_call("notebooks/", exist_ok=True)
        mock_makedirs.assert_any_call("queries/", exist_ok=True)
        mock_makedirs.assert_any_call("src/jobs/", exist_ok=True)

        mock_dockerfile.buildDockerfile.assert_called_once()
        mock_dignore.buildDockerignore.assert_called_once()
        mock_readme.buildREADME.assert_called_once()
        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.Config')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerfile')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerignore')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.readme')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_container(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_makedirs,
                              mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", "Default", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Select a TEMPLATE", options=["Dash", "Package", "Default"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.load.assert_called_once()

        mock_makedirs.assert_any_call("config/", exist_ok=True)
        mock_makedirs.assert_any_call("data/", exist_ok=True)
        mock_makedirs.assert_any_call("notebooks/", exist_ok=True)
        mock_makedirs.assert_any_call("queries/", exist_ok=True)
        mock_makedirs.assert_any_call("src/jobs/", exist_ok=True)

        mock_dockerfile.buildDockerfile.assert_called_once()
        mock_dignore.buildDockerignore.assert_called_once()
        mock_readme.buildREADME.assert_called_once()
        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.Config')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerfile')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerignore')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.readme')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_package(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_makedirs,
                              mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", "Package", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Select a TEMPLATE", options=["Dash", "Package", "Default"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.load.assert_called_once()

        mock_makedirs.assert_any_call("test/", exist_ok=True)

        mock_dockerfile.buildDockerfile.assert_called_once()
        mock_dignore.buildDockerignore.assert_called_once()
        mock_readme.buildREADME.assert_called_once()
        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('os.path.expanduser')
    @mock.patch('os.path.exists')
    @mock.patch('os.getcwd')
    @mock.patch('os.makedirs')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.open')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.Config')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.ComponentFactory')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerfile')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.dockerignore')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.readme')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.yaml')
    @mock.patch('skelebot.systems.scaffolding.scaffolder.promptUser')
    def test_execute_scaffold_dash(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_open,
                              mock_makedirs, mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", "Dash", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        #sb.systems.scaffolding.scaffolder.scaffold(existing=False)
        scaffolder = sb.systems.scaffolding.scaffolder.Scaffolder(existing=False)
        scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Select a LANGUAGE", options=["Python", "R", "R+Python"])
        mock_prompt.assert_any_call("Select a TEMPLATE", options=["Dash", "Package", "Default"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.load.assert_called_once()

        mock_makedirs.assert_any_call("src/assets/", exist_ok=True)
        dirname = os.path.dirname(__file__)
        dirname = dirname[:len(dirname) - 5]
        mock_open.assert_any_call(os.path.join(dirname, "skelebot/systems/scaffolding/templates/dash/app_py"), "r")
        mock_open.assert_any_call("src/app.py", "w")
        mock_open.assert_any_call(os.path.join(dirname, "skelebot/systems/scaffolding/templates/dash/server_py"), "r")
        mock_open.assert_any_call("src/server.py", "w")
        mock_open.assert_any_call(os.path.join(dirname, "skelebot/systems/scaffolding/templates/dash/config_py"), "r")
        mock_open.assert_any_call("src/config.py", "w")
        mock_open.assert_any_call(os.path.join(dirname, "skelebot/systems/scaffolding/templates/dash/style_css"), "r")
        mock_open.assert_any_call("src/assets/style.css", "w")

        mock_dockerfile.buildDockerfile.assert_called_once()
        mock_dignore.buildDockerignore.assert_called_once()
        mock_readme.buildREADME.assert_called_once()
        mock_yaml.saveConfig.assert_called_once()

    @mock.patch('skelebot.systems.scaffolding.prompt.input')
    def test_scaffold_prompt(self, mock_input):
        mock_input.return_value = "hi"

        msg = sb.systems.scaffolding.prompt.promptUser("Enter A Message")

        mock_input.assert_called_with("Enter A Message: ")
        self.assertEqual(msg, "hi")

    @mock.patch('skelebot.systems.scaffolding.prompt.input')
    def test_scaffold_prompt_options(self, mock_input):
        mock_input.return_value = "rf"

        msg = sb.systems.scaffolding.prompt.promptUser("Select an Algorithm", options=["glm", "rf", "lgbm"])

        mock_input.assert_called_with("Select an Algorithm [glm, rf, lgbm]: ")
        self.assertEqual(msg, "rf")

    def test_scaffold_prompt_option(self):
        msg = sb.systems.scaffolding.prompt.promptUser("Select an Algorithm", options=["glm"])

        self.assertEqual(msg, "glm")

    @mock.patch('skelebot.systems.scaffolding.prompt.input')
    def test_scaffold_prompt_boolean(self, mock_input):
        mock_input.return_value = "Y"

        msg = sb.systems.scaffolding.prompt.promptUser("Would you like CHEESE with that?", boolean=True)

        mock_input.assert_called_with("Would you like CHEESE with that? [Y/N]: ")
        self.assertTrue(msg)

    @mock.patch('skelebot.systems.scaffolding.prompt.input')
    def test_scaffold_prompt_boolean_false(self, mock_input):
        mock_input.return_value = "n"

        msg = sb.systems.scaffolding.prompt.promptUser("Would you like CHEESE with that?", boolean=True)

        mock_input.assert_called_with("Would you like CHEESE with that? [Y/N]: ")
        self.assertFalse(msg)

if __name__ == '__main__':
    unittest.main()
