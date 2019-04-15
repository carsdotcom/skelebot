from unittest import TestCase
from unittest import mock
import skelebot as sb

class TestScaffold(TestCase):

    # Test that the Scaffolding process can be run iwthout errors
    @mock.patch('os.chmod')
    @mock.patch('os.stat')
    @mock.patch('os.makedirs')
    @mock.patch('os.listdir')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('builtins.open')
    @mock.patch('builtins.input')
    def test_Scaffold(self, mock_input, mock_open, mock_expand, mock_exists, mock_listdr, mock_mkdirs, mock_stat, mock_chmod):
        return_values = ["project name", "desc", "ME", "my-email@mial.com", "Python",
                         "y", "model", "model.pkl", "art.com", "repo", "path",
                         "y", "me", "me.keytab", "krb5.conf",
                         "y"]

        def f(message):
            mock_input.return_value = return_values[mock_input.call_count-1]
            return return_values[mock_input.call_count-1]

        mock_input.side_effect = f
        mock_expand.return_value = "/"
        mock_exists.return_value = True
        mock_listdr.return_value = []
        mock_open.return_value = mock.Mock()
        st = mock.Mock()
        st.st_mode = 1
        mock_stat.return_value = st

        sb.scaffold.scaffold(".")

if __name__ == '__main__':
    unittest.main()
