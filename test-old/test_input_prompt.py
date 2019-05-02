from unittest import TestCase
from unittest import mock
import skelebot as sb

class TestInputPromptUser(TestCase):

    # Test that the prompt returns the proper input
    @mock.patch('builtins.input')
    def test_promptUser(self, mock_input):
        message = "Enter your NAME"
        mock_input.return_value = 'ME'

        name = sb.input.prompt.promptUser(message)
        self.assertEqual("ME", name)
        mock_input.assert_called_with('Enter your NAME: ')

    # Test that the prompt returns the proper input for the options
    @mock.patch('builtins.input')
    def test_promptUserOptions(self, mock_input):
        message = "How many fries would you like"
        options = [1, 5, 10, 100, 5000]
        return_values = ["2", "3", "10"]

        def f(message):
            mock_input.return_value = return_values[mock_input.call_count-1]
            return return_values[mock_input.call_count-1]

        mock_input.side_effect = f

        fries = sb.input.prompt.promptUser(message, options=options)
        self.assertEqual("10", fries)
        mock_input.assert_called_with('How many fries would you like [1, 5, 10, 100, 5000]: ')

    # Test that the prompt returns the proper input for the boolean
    @mock.patch('builtins.input')
    def test_promptUserBoolean(self, mock_input):
        message = "Would you like fries with that"
        mock_input.return_value = 'y'

        likeFries = sb.input.prompt.promptUser(message, boolean=True)
        self.assertEqual(True, likeFries)
        mock_input.assert_called_with('Would you like fries with that [Y/N]: ')

if __name__ == '__main__':
    unittest.main()
