from unittest import TestCase
from unittest import mock

import skelebot as sb
import argparse
import os
import shutil

class TestArtifactory(TestCase):
    artifcatory = None

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

        expectedException = """This artifact version has already been pushed.
Please bump the version before pushing (skelebot bump) or force push (-f)."""

        try:
            self.artifactory.execute(config, args)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), expectedException)


    @mock.patch('shutil.copyfile')
    @mock.patch('os.remove')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_push(self, mock_artifactory, mock_remove, mock_copy):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="push", force=True, artifact='test', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v1.0.0.pkl", auth=(None, None))
        mock_copy.assert_called_with("test.pkl", "test_v1.0.0.pkl")
        mock_remove.assert_called_with("test_v1.0.0.pkl")

    @mock.patch('builtins.open')
    @mock.patch('artifactory.ArtifactoryPath')
    def test_execute_pull(self, mock_artifactory, mock_open):
        config = sb.objects.config.Config(version="1.0.0")
        args = argparse.Namespace(job="pull", version='0.1.0', artifact='test', user='sean', token='abc123')

        self.artifactory.execute(config, args)

        mock_artifactory.assert_called_with("artifactory.test.com/ml/test/test_v0.1.0.pkl", auth=(None, None))
        mock_open.assert_called_with("test_v0.1.0.pkl", "wb")

if __name__ == '__main__':
    unittest.main()
