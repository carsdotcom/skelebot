from unittest import TestCase, main, mock
from schema import SchemaError
import copy
import argparse
import skelebot as sb

class TestRepository(TestCase):

    artifcatory = None
    s3 = None
    s3_subfolder = None

    artifactoryDict = {
        "url": "test",
        "repo": "test",
        "path": "path"
    }

    s3Dict = {
        "bucket": "my-bucket",
        "region": "us-east-1",
        "profile": "test"
    }

    artifactDict = {
        "name": "test",
        "file": "test"
    }

    def setUp(self):
        artifact = sb.components.repository.repository.Artifact("test", "test.pkl")
        artifact2 = sb.components.repository.repository.Artifact("test2", "test2.pkl")
        artifact3 = sb.components.repository.repository.Artifact("test3", "test3.pkl", singular=True)
        artifactoryRepo = sb.components.repository.artifactoryRepo.ArtifactoryRepo("artifactory.test.com", "ml", "test")
        s3Repo = sb.components.repository.s3Repo.S3Repo("my-bucket", "us-east-1", "test")
        s3Repo_path = sb.components.repository.s3Repo.S3Repo("my-bucket/sub/folder", "us-east-1", "test")

        self.artifactory = sb.components.repository.repository.Repository([artifact, artifact2, artifact3], s3=None, artifactory=artifactoryRepo)
        self.s3 = sb.components.repository.repository.Repository([artifact, artifact2, artifact3], s3=s3Repo, artifactory=None)
        self.s3_subfolder = sb.components.repository.repository.Repository([artifact, artifact3], s3=s3Repo_path, artifactory=None)

    def test_repository_load(self):
        artifact = sb.components.repository.repository.Artifact("test", "test.pkl")

        sb.components.repository.repository.Repository.load({"artifacts": [], "s3": self.s3Dict})
        sb.components.repository.repository.Repository.load({"artifacts": [], "artifactory": self.artifactoryDict})

        try:
            sb.components.repository.repository.Repository.load({"artifacts": []})
            self.fail("Exception Not Thrown")
        except SchemaError as exc:
            self.assertEqual(str(exc), "Repository must contain 's3' or 'artifactory' config")

    def test_addParsers_artifactory(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = self.artifactory.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["push"], None)
        self.assertNotEqual(subparsers.choices["pull"], None)

    def test_addParsers_s3(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = self.s3.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["push"], None)
        self.assertNotEqual(subparsers.choices["pull"], None)

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('os.rename')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_conflict_artifactory(self, mock_artifactory, mock_rename, mock_input):
        mock_input.return_value = "abc"
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=False, artifact='test', user=None, token=None)
        expectedException = "This artifact version already exists. Please bump the version or use the force parameter (-f) to overwrite the artifact."

        try:
            self.artifactory.execute(config, args)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), expectedException)
            mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('abc', 'abc'))

    @mock.patch('boto3.Session')
    def test_execute_push_conflict_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_client.list_objects_v2.return_value = {"Contents": [{"Key": "test_v1.0.0.pkl"}]}
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=False, artifact='test', user='sean', token='abc123')
        expectedException = "This artifact version already exists. Please bump the version or use the force parameter (-f) to overwrite the artifact."

        try:
            self.s3.execute(config, args)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), expectedException)
            mock_client.list_objects_v2.assert_called_with(Bucket="my-bucket", Prefix="test_v1.0.0.pkl")

    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_error_artifactory(self, mock_artifactory, mock_remove, mock_copy):
        mock_path = mock.MagicMock()
        mock_path.deploy_file = mock.MagicMock(side_effect=KeyError('foo'))
        mock_artifactory.return_value = mock_path

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        with self.assertRaises(KeyError):
            self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('sean', 'abc123'))
        mock_copy.assert_called_with("test.pkl", "test_v1.0.0.pkl")
        mock_remove.assert_called_with("test_v1.0.0.pkl")

    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_artifactory(self, mock_artifactory, mock_remove, mock_copy):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('sean', 'abc123'))
        mock_copy.assert_called_with("test.pkl", "test_v1.0.0.pkl")
        mock_remove.assert_called_with("test_v1.0.0.pkl")

    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_artifactory_singular(self, mock_artifactory, mock_remove, mock_copy):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test3', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test3.pkl", auth=('sean', 'abc123'))
        mock_copy.assert_called_with("test3.pkl", "test3.pkl")
        mock_remove.assert_called_with("test3.pkl")

    @mock.patch('boto3.Session')
    def test_execute_push_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        self.s3.execute(config, args)
        mock_client.upload_file.assert_called_with("test.pkl", "my-bucket", "test_v1.0.0.pkl")

    @mock.patch('boto3.Session')
    def test_execute_push_s3_singular(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test3', user='sean', token='abc123')

        self.s3.execute(config, args)
        mock_client.upload_file.assert_called_with("test3.pkl", "my-bucket", "test3.pkl")

    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_artifactory_all(self, mock_artifactory, mock_remove, mock_copy):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='ALL', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_has_calls([
            mock.call("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('sean', 'abc123')),
            mock.call("artifactory.test.com/ml/test/test2_v1.0.0.pkl", auth=('sean', 'abc123'))
        ], any_order=True)
        mock_copy.assert_has_calls([
            mock.call("test.pkl", "test_v1.0.0.pkl"),
            mock.call("test2.pkl", "test2_v1.0.0.pkl")
        ], any_order=True)
        mock_remove.assert_has_calls([
            mock.call("test_v1.0.0.pkl"),
            mock.call("test2_v1.0.0.pkl")
        ], any_order=True)

    @mock.patch('boto3.Session')
    def test_execute_push_s3_all(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='ALL', user='sean', token='abc124')

        self.s3.execute(config, args)
        mock_client.upload_file.assert_has_calls([
            mock.call("test.pkl", "my-bucket", "test_v1.0.0.pkl"),
            mock.call("test2.pkl", "my-bucket", "test2_v1.0.0.pkl")
        ], any_order=True)

    @mock.patch('boto3.Session')
    def test_execute_push_s3_subfolder(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        self.s3_subfolder.execute(config, args)
        mock_client.upload_file.assert_called_with("test.pkl", "my-bucket", "sub/folder/test_v1.0.0.pkl")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_artifactory(self, mock_artifactory, mock_open, mock_input):
        mock_input.return_value = "abc"

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.1.0.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test_v0.1.0.pkl", "wb")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_artifactory_singular(self, mock_artifactory, mock_open, mock_input):
        mock_input.return_value = "abc"

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test3', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test3.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test3.pkl", "wb")

    @mock.patch('boto3.Session')
    def test_execute_pull_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user=None, token=None, override=False)

        self.s3.execute(config, args)
        mock_client.download_file.assert_called_with("my-bucket", "test_v0.1.0.pkl", "test_v0.1.0.pkl")

    @mock.patch('boto3.Session')
    def test_execute_pull_s3_subfolder(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user=None, token=None, override=False)

        self.s3_subfolder.execute(config, args)
        mock_client.download_file.assert_called_with("my-bucket", "sub/folder/test_v0.1.0.pkl", "test_v0.1.0.pkl")

    @mock.patch('boto3.Session')
    def test_execute_pull_s3_subfolder_singular(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test3', user=None, token=None, override=False)

        self.s3_subfolder.execute(config, args)
        mock_client.download_file.assert_called_with("my-bucket", "sub/folder/test3.pkl", "test3.pkl")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_lcv_artifactory(self, mock_artifactory, mock_open, mock_input):
        mock_apath = mock_artifactory.return_value
        mock_input.return_value = "abc"
        mock_apath.__iter__.return_value = ["test_v1.1.0", "test_v0.2.4", "test_v1.0.0", "test_v2.0.1"]

        config = sb.objects.config.Config(version="1.0.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test_v1.0.0.pkl", "wb")

    @mock.patch('boto3.Session')
    def test_execute_pull_lcv_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_client.list_objects_v2.return_value = {"Contents": [{"Key": "test_v1.1.0.pkl"},{"Key": "test_v1.0.5.pkl"},{"Key": "test_v1.0.0.pkl"}]}
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=False)

        self.s3.execute(config, args)

        mock_client.list_objects_v2.assert_called_with(Bucket="my-bucket", Prefix="test_v1")
        mock_client.download_file.assert_called_with("my-bucket", "test_v1.0.5.pkl", "test_v1.0.5.pkl")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_lcv_not_found_artifactory(self, mock_artifactory, mock_open, mock_input):
        mock_apath = mock_artifactory.return_value
        mock_input.return_value = "abc"
        mock_apath.__iter__.return_value = ["test_v1.1.0", "test_v0.2.4", "test_v1.0.0", "test_v2.0.1"]

        config = sb.objects.config.Config(version="3.0.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=False)

        try:
            self.artifactory.execute(config, args)
            self.fail("Exception Not Thrown")
        except RuntimeError as err:
            self.assertEqual(str(err), "No Compatible Version Found")

    @mock.patch('boto3.Session')
    def test_execute_pull_lcv_not_found_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_client.list_objects_v2.return_value = {"Contents": [{"Key": "test_v1.1.0.pkl"},{"Key": "test_v1.0.5.pkl"},{"Key": "test_v1.0.0.pkl"}]}
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="2.0.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=False)

        try:
            self.s3.execute(config, args)
            self.fail("Exception Not Thrown")
        except RuntimeError as err:
            self.assertEqual(str(err), "No Compatible Version Found")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_override_and_lcv_artifactory(self, mock_artifactory, mock_open, mock_input):
        mock_apath = mock_artifactory.return_value
        mock_input.return_value = "abc"
        mock_apath.__iter__.return_value = ["test_v1.1.0", "test_v0.2.4", "test_v1.0.0", "test_v2.0.1"]

        config = sb.objects.config.Config(version="0.6.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=True)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.2.4.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test.pkl", "wb")

    @mock.patch('boto3.Session')
    def test_execute_pull_override_and_lcv_s3(self, mock_boto3_session):
        mock_client = mock.Mock()
        mock_session = mock.Mock()
        mock_client.list_objects_v2.return_value = {"Contents": [{"Key": "test_v1.1.0.pkl"},{"Key": "test_v1.0.5.pkl"},{"Key": "test_v1.0.0.pkl"}]}
        mock_session.client.return_value = mock_client
        mock_boto3_session.return_value = mock_session

        config = sb.objects.config.Config(version="1.0.3")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=True)

        self.s3.execute(config, args)

        mock_client.download_file.assert_called_with("my-bucket", "test_v1.0.0.pkl", "test.pkl")

    @mock.patch('skelebot.components.repository.artifactoryRepo.input')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_not_found(self, mock_artifactory, mock_input):
        mock_input.return_value = "abc"
        path = mock_artifactory.return_value
        path.exists.return_value = False

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.1.0.pkl", auth=("abc", "abc"))

    def test_validate_valid(self):
        try:
            sb.components.repository.artifactoryRepo.ArtifactoryRepo.validate(self.artifactoryDict)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

        try:
            sb.components.repository.s3Repo.S3Repo.validate(self.s3Dict)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

        try:
            sb.components.repository.repository.Artifact.validate(self.artifactDict)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_validate_missing(self):
        s3Dict = copy.deepcopy(self.s3Dict)
        del s3Dict['bucket']
        del s3Dict['region']
        del s3Dict['profile']

        try:
            sb.components.repository.s3Repo.S3Repo.validate(s3Dict)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'bucket', 'region'")

        artifactoryDict = copy.deepcopy(self.artifactoryDict)
        del artifactoryDict['url']
        del artifactoryDict['repo']
        del artifactoryDict['path']

        try:
            sb.components.repository.artifactoryRepo.ArtifactoryRepo.validate(artifactoryDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'path', 'repo', 'url'")

        artifactDict = copy.deepcopy(self.artifactDict)
        del artifactDict['name']
        del artifactDict['file']

        try:
            sb.components.repository.repository.Artifact.validate(artifactDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'file', 'name'")

    def validate_error_s3(self, attr, reset, expected):
        s3Dict = copy.deepcopy(self.s3Dict)
        s3Dict[attr] = reset

        try:
            sb.components.repository.s3Repo.S3Repo.validate(s3Dict)
        except SchemaError as error:
            self.assertEqual(error.code, "S3 '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def validate_error_artifactory(self, attr, reset, expected):
        artifactoryDict = copy.deepcopy(self.artifactoryDict)
        artifactoryDict[attr] = reset

        try:
            sb.components.repository.artifactoryRepo.ArtifactoryRepo.validate(artifactoryDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Artifactory '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def validate_error_artifact(self, attr, reset, expected):
        artifactDict = copy.deepcopy(self.artifactDict)
        artifactDict[attr] = reset

        try:
            sb.components.repository.repository.Artifact.validate(artifactDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Artifact '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def test_invalid(self):
        self.validate_error_s3('bucket', 123, 'String')
        self.validate_error_s3('region', 123, 'String')
        self.validate_error_s3('profile', 123, 'String')
        self.validate_error_artifactory('url', 123, 'String')
        self.validate_error_artifactory('repo', 123, 'String')
        self.validate_error_artifactory('path', 123, 'String')
        self.validate_error_artifact('name', 123, 'String')
        self.validate_error_artifact('file', 123, 'String')

if __name__ == '__main__':
    main()
