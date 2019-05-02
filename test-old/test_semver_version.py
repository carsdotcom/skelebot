from unittest import TestCase
import skelebot as sb

class TestVersion(TestCase):

    # Setup the Config Object
    def setUp(self):
        args = [sb.config.Param("date", None, None, None)]
        params = [sb.config.Param("env", "e", "local", ["local", "dev", "prod"])]
        defaultJobs = [sb.config.Job("example", "src/jobs/example.job", "EXAMPLE JOB", args, params)]
        kerberos = sb.config.Kerberos("me", "me.keytab", "krb5.conf")
        self.config = sb.config.Config("test", "test proj", "0.1.0", "1.0.0", "me", "me@email.com", "R", kerberos, None, ["stringr", "readr"], [".RData", ".pkl"], defaultJobs, None, None, False, None)

    def test_bumpPatch(self):
        config = self.config

        config = sb.version.bumpVersion(self.config, "patch")
        self.assertEqual("0.1.1", config.version)

        config = sb.version.bumpVersion(self.config, "patch")
        self.assertEqual("0.1.2", config.version)

    def test_bumpMinor(self):
        config = self.config

        config = sb.version.bumpVersion(self.config, "minor")
        self.assertEqual("0.2.0", config.version)

        config = sb.version.bumpVersion(self.config, "minor")
        self.assertEqual("0.3.0", config.version)

    def test_bumpMajor(self):
        config = self.config

        config = sb.version.bumpVersion(self.config, "major")
        self.assertEqual("1.0.0", config.version)

        config = sb.version.bumpVersion(self.config, "major")
        self.assertEqual("2.0.0", config.version)

if __name__ == '__main__':
    unittest.main()
