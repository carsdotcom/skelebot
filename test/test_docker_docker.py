from unittest import TestCase
import skelebot as sb

class TestDocker(TestCase):

    # Setup the Config Object
    def setUp(self):
        args = [sb.config.Param("date", None, None, None)]
        params = [sb.config.Param("env", "e", "local", ["local", "dev", "prod"])]
        defaultJobs = [sb.config.Job("example", "src/jobs/example.job", "EXAMPLE JOB", args, params)]
        kerberos = sb.config.Kerberos("me", "me.keytab", "krb5.conf")
        copy = ["here:there", "also/here:and/there"]
        self.configR = sb.config.Config("test", "test proj", "0.1", "1.0.0", "me", "me@email.com", "R", kerberos,
                                ["apt-get install pip"], ["stringr", "readr"], [".RData", ".pkl"], defaultJobs, None, copy, False, None)
        self.configPython = sb.config.Config("test", "test proj", "0.1", "1.0.0", "me", "me@email.com", "Python",
                                kerberos, None, ["scipy", "pandas"], [".RData", ".pkl"], defaultJobs, None, copy, False, None)

    # Test that the R dockerfile is built properly
    def test_buildDockerfileR(self):
        actual = sb.docker.buildDockerfile(self.configR)
        self.assertTrue("# This Dockerfile was generated by Skelebot" in actual)
        self.assertTrue("# Editing this file manually is not advised as all changes will be overwritten during Skelebot execution" in actual)
        self.assertTrue("FROM skelebot/r-krb" in actual)
        self.assertTrue("MAINTAINER me <me@email.com>" in actual)
        self.assertTrue("WORKDIR /app" in actual)
        self.assertTrue("RUN [\"apt-get\", \"install\", \"pip\"]" in actual)
        self.assertTrue("RUN [\"Rscript\", \"-e\", \"install.packages('stringr', repo='https://cloud.r-project.org'); library(stringr)\"]" in actual)
        self.assertTrue("RUN [\"Rscript\", \"-e\", \"install.packages('readr', repo='https://cloud.r-project.org'); library(readr)\"]" in actual)
        self.assertTrue("COPY here there" in actual)
        self.assertTrue("COPY also/here and/there" in actual)
        self.assertTrue("COPY krb5.conf /etc/krb5.conf" in actual)

    # Test that the Python dockerfile is built properly
    def test_buildDockerfilePython(self):
        actual = sb.docker.buildDockerfile(self.configPython)
        self.assertTrue("# This Dockerfile was generated by Skelebot" in actual)
        self.assertTrue("# Editing this file manually is not advised as all changes will be overwritten during Skelebot execution" in actual)
        self.assertTrue("FROM skelebot/python-krb" in actual)
        self.assertTrue("MAINTAINER me <me@email.com>" in actual)
        self.assertTrue("WORKDIR /app" in actual)
        self.assertTrue("RUN [\"pip\", \"install\", \"scipy\"]" in actual)
        self.assertTrue("RUN [\"pip\", \"install\", \"pandas\"]" in actual)
        self.assertTrue("COPY here there" in actual)
        self.assertTrue("COPY also/here and/there" in actual)
        self.assertTrue("COPY krb5.conf /etc/krb5.conf" in actual)

if __name__ == '__main__':
    unittest.main()