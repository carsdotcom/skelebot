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
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", False]

        try:
            sb.systems.scaffolding.scaffolder.scaffold(False)
            self.fail("Exception Expected")
        except Exception as exc:
            self.assertEqual(str(exc), "Aborting Scaffolding Process")

            mock_prompt.assert_any_call("Enter a PROJECT NAME")
            mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
            mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
            mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
            mock_prompt.assert_any_call("Enter a LANGUAGE", options=["Python", "R","R+Python"])
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
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", True]

        sb.systems.scaffolding.scaffolder.scaffold(True)

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Enter a LANGUAGE", options=["Python", "R","R+Python"])
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
    def test_execute_scaffold(self, mock_prompt, mock_yaml, mock_readme, mock_dignore,
                              mock_dockerfile, mock_cFactory, mock_config, mock_makedirs,
                              mock_getcwd, mock_exists, mock_expanduser):
        mock_expanduser.return_value = "test/plugins"
        mock_prompt.side_effect = ["test", "test proj", "sean", "email", "Python", True]

        # Set up mock components with scaffolding
        mock_single_comp = mock.MagicMock()
        mock_single_comp.scaffold.return_value = 'foo'
        mock_list_comp = mock.MagicMock()
        mock_list_comp.scaffold.return_value = ['bar', 'baz']

        mock_cFactory.return_value.buildComponents.return_value = [
            mock_single_comp, mock_list_comp
        ]

        sb.systems.scaffolding.scaffolder.scaffold()

        mock_prompt.assert_any_call("Enter a PROJECT NAME")
        mock_prompt.assert_any_call("Enter a PROJECT DESCRIPTION")
        mock_prompt.assert_any_call("Enter a MAINTAINER NAME")
        mock_prompt.assert_any_call("Enter a CONTACT EMAIL")
        mock_prompt.assert_any_call("Enter a LANGUAGE", options=["Python", "R","R+Python"])
        mock_prompt.assert_any_call("Confirm Skelebot Setup", boolean=True)

        mock_config.assert_called_once()
        self.assertEqual(['foo', 'bar', 'baz'], mock_config.call_args[1]['components'])

        mock_makedirs.assert_any_call("config/", exist_ok=True)
        mock_makedirs.assert_any_call("data/", exist_ok=True)
        mock_makedirs.assert_any_call("models/", exist_ok=True)
        mock_makedirs.assert_any_call("notebooks/", exist_ok=True)
        mock_makedirs.assert_any_call("output/", exist_ok=True)
        mock_makedirs.assert_any_call("queries/", exist_ok=True)
        mock_makedirs.assert_any_call("src/jobs/", exist_ok=True)

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
