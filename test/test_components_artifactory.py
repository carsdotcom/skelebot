import argparse
import copy
import unittest
from unittest import mock

from schema import SchemaError

import skelebot as sb

class TestArtifactory(unittest.TestCase):
    artifcatory = None

    artifactoryDict = {
        "url": "test",
        "repo": "test",
        "path": "path",
        "artifacts": [1, 2]
    }

    artifactDict = {
        "name": "test",
        "file": "test"
    }

    def setUp(self):
        artifact = sb.components.artifactory.Artifact("test", "test.pkl")
        self.artifactory = sb.components.artifactory.Artifactory([artifact], "artifactory.test.com", "ml", "test")

    def test_addParsers(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest="job")
        subparsers = self.artifactory.addParsers(subparsers)

        self.assertNotEqual(subparsers.choices["push"], None)
        self.assertNotEqual(subparsers.choices["pull"], None)

    @mock.patch('os.rename')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_conflict(self, mock_artifactory, mock_rename):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=False, artifact='test', user='sean', token='abc123')

        expectedException = "This artifact version already exists. Please bump the version or use the force parameter (-f) to overwrite the artifact."

        try:
            self.artifactory.execute(config, args)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), expectedException)
            mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('sean', 'abc123'))

    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push_error(self, mock_artifactory, mock_remove, mock_copy):
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
    def test_execute_push(self, mock_artifactory, mock_remove, mock_copy):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=('sean', 'abc123'))
        mock_copy.assert_called_with("test.pkl", "test_v1.0.0.pkl")
        mock_remove.assert_called_with("test_v1.0.0.pkl")

    @mock.patch('skelebot.components.artifactory.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull(self, mock_artifactory, mock_open, mock_input):
        mock_input.return_value = "abc"

        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.1.0.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test_v0.1.0.pkl", "wb")

    @mock.patch('skelebot.components.artifactory.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_lcv(self, mock_artifactory, mock_open, mock_input):
        mock_apath = mock_artifactory.return_value
        mock_input.return_value = "abc"
        mock_apath.__iter__.return_value = ["test_v1.1.0", "test_v0.2.4", "test_v1.0.0", "test_v2.0.1"]

        config = sb.objects.config.Config(version="1.0.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=False)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test_v1.0.0.pkl", "wb")

    @mock.patch('skelebot.components.artifactory.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_lcv_not_found(self, mock_artifactory, mock_open, mock_input):
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

    @mock.patch('skelebot.components.artifactory.input')
    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull_override_and_lcv(self, mock_artifactory, mock_open, mock_input):
        mock_apath = mock_artifactory.return_value
        mock_input.return_value = "abc"
        mock_apath.__iter__.return_value = ["test_v1.1.0", "test_v0.2.4", "test_v1.0.0", "test_v2.0.1"]

        config = sb.objects.config.Config(version="0.6.9")
        args = argparse.Namespace(job="pull", version='LATEST', artifact='test', user=None, token=None, override=True)

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.2.4.pkl", auth=("abc", "abc"))
        mock_open.assert_called_with("test.pkl", "wb")

    @mock.patch('skelebot.components.artifactory.input')
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
            sb.components.artifactory.Artifactory.validate(self.artifactoryDict)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

        try:
            sb.components.artifactory.Artifact.validate(self.artifactDict)
        except:
            self.fail("Validation Raised Exception Unexpectedly")

    def test_validate_mising(self):
        artifactoryDict = copy.deepcopy(self.artifactoryDict)
        del artifactoryDict['url']
        del artifactoryDict['repo']
        del artifactoryDict['path']

        try:
            sb.components.artifactory.Artifactory.validate(artifactoryDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'path', 'repo', 'url'")

        artifactDict = copy.deepcopy(self.artifactDict)
        del artifactDict['name']
        del artifactDict['file']

        try:
            sb.components.artifactory.Artifact.validate(artifactDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Missing keys: 'file', 'name'")

    def validate_error_artifactory(self, attr, reset, expected):
        artifactoryDict = copy.deepcopy(self.artifactoryDict)
        artifactoryDict[attr] = reset

        try:
            sb.components.artifactory.Artifactory.validate(artifactoryDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Artifactory '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def validate_error_artifact(self, attr, reset, expected):
        artifactDict = copy.deepcopy(self.artifactDict)
        artifactDict[attr] = reset

        try:
            sb.components.artifactory.Artifact.validate(artifactDict)
        except SchemaError as error:
            self.assertEqual(error.code, "Artifact '{attr}' must be a {expected}".format(attr=attr, expected=expected))

    def test_invalid(self):
        self.validate_error_artifactory('url', 123, 'String')
        self.validate_error_artifactory('repo', 123, 'String')
        self.validate_error_artifactory('path', 123, 'String')
        self.validate_error_artifactory('artifacts', 123, 'List')
        self.validate_error_artifact('name', 123, 'String')
        self.validate_error_artifact('file', 123, 'String')

if __name__ == '__main__':
    unittest.main()
