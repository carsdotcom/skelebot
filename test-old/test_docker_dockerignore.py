from unittest import TestCase
import skelebot as sb

class TestDockerDockerignore(TestCase):

    # Test that the dockerignore text is built based on the global ignore config
    def test_buildDockerignore(self):
        ignore = ["*.RData", "*.pkl", "*.csv"]
        cfg = sb.config.Config("All My Code", "proj", "2", "1", "me", "me", "R", None, None, None, ignore, None, None, None, "False", None)
        dignore = sb.dockerignore.buildDockerignore(cfg)
        expected = "*.RData\n*.pkl\n*.csv"
        self.assertEqual(expected, dignore)

    # Test that the dockerignore text is built based on the global ignore config and the job ignore
    def test_buildDockerignoreWithJob(self):
        ignore = ["*.RData", "*.pkl", "*.csv"]
        job = sb.config.Job("run", "run.sh", "run the job", None, None, ["one", "two", "three"], "i")
        jobs = [job]
        cfg = sb.config.Config("All My Code", "proj", "2", "1", "me", "me", "R", None, None, None, ignore, jobs, None, None, "False", None)
        dignore = sb.dockerignore.buildDockerignore(cfg, job)
        expected = "*.RData\n*.pkl\n*.csv\none\ntwo\nthree"
        self.assertEqual(expected, dignore)

if __name__ == '__main__':
    unittest.main()
