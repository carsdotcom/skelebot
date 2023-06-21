from unittest import TestCase, main, mock
import skelebot as sb

class TestAuth(TestCase):

    @mock.patch('boto3.Session')
    def test_load_aws_credentials(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_boto3_session.return_value = mock_session
        mock_session.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {"SecretString": '{"a": 1}'}

        auth = sb.components.repository.artifactoryRepo.Auth(
            aws=True, awsSecret="foo", awsProfile="bar", awsRegion="baz"
        )
        actual_creds = auth.loadAwsCredentials()

        assert actual_creds == {"a": 1}
        mock_client.get_secret_value.assert_called_with(SecretId="foo")
        mock_session.client.assert_called_with(service_name="secretsmanager", region_name="baz")
        mock_boto3_session.assert_called_with(profile_name="bar")

    @mock.patch('boto3.Session')
    def test_load_aws_default_credentials(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_boto3_session.return_value = mock_session
        mock_session.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {"SecretString": '{"a": 1}'}

        auth = sb.components.repository.artifactoryRepo.Auth(aws=True)
        actual_creds = auth.loadAwsCredentials()

        assert actual_creds == {"a": 1}
        mock_client.get_secret_value.assert_called_with(SecretId="Artifactory")
        mock_session.client.assert_called_with(service_name="secretsmanager", region_name="us-east-1")
        mock_boto3_session.assert_called_with(profile_name=None)

    @mock.patch('boto3.Session')
    def test_get_credentials_aws_user_pass(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_boto3_session.return_value = mock_session
        mock_session.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "SecretString": '{"user": "abc", "token": "def"}'
        }

        auth = sb.components.repository.artifactoryRepo.Auth(
            authType="user_pass", aws=True, awsSecret="foo", awsProfile="bar", awsRegion="baz"
        )

        actual_creds = auth.getCredentials()
        assert actual_creds == {"auth": ("abc", "def")}
        mock_client.get_secret_value.assert_called_with(SecretId="foo")
        mock_session.client.assert_called_with(service_name="secretsmanager", region_name="baz")
        mock_boto3_session.assert_called_with(profile_name="bar")

    @mock.patch('boto3.Session')
    def test_get_credentials_aws_token(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_boto3_session.return_value = mock_session
        mock_session.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            "SecretString": '{"token": "def"}'
        }

        auth = sb.components.repository.artifactoryRepo.Auth(
            authType="token", aws=True, awsSecret="foo", awsProfile="bar", awsRegion="baz"
        )

        actual_creds = auth.getCredentials()
        assert actual_creds == {"token": "def"}
        mock_client.get_secret_value.assert_called_with(SecretId="foo")
        mock_session.client.assert_called_with(service_name="secretsmanager", region_name="baz")
        mock_boto3_session.assert_called_with(profile_name="bar")

    @mock.patch('skelebot.components.repository.artifactoryRepo.getpass')
    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    def test_get_credentials_input_user_pass(self, mock_input, mock_pass):
        mock_input.return_value = "abc"
        mock_pass.return_value = "def"

        auth = sb.components.repository.artifactoryRepo.Auth(authType="user_pass")
        actual_creds = auth.getCredentials()

        assert actual_creds == {"auth": ("abc", "def")}
        mock_input.assert_called_with("Please provide a valid Artifactory user: ")
        mock_pass.assert_called_with("Please provide a valid Artifactory password: ")

    @mock.patch('skelebot.components.repository.artifactoryRepo.getpass')
    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    def test_get_credentials_input_token(self, mock_input, mock_pass):
        mock_pass.return_value = "abc"

        auth = sb.components.repository.artifactoryRepo.Auth(authType="token")
        actual_creds = auth.getCredentials()

        assert actual_creds == {"token": "abc"}
        mock_input.asser_not_called()
        mock_pass.assert_called_with("Please provide a valid Artifactory token: ")

    @mock.patch('skelebot.components.repository.artifactoryRepo.getpass')
    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    def test_get_credentials_input_apikey(self, mock_input, mock_pass):
        mock_pass.return_value = "abc"

        auth = sb.components.repository.artifactoryRepo.Auth(authType="apikey")
        actual_creds = auth.getCredentials()

        assert actual_creds == {"apikey": "abc"}
        mock_input.asser_not_called()
        mock_pass.assert_called_with("Please provide a valid Artifactory apikey: ")

if __name__ == '__main__':
    main()
