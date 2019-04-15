from unittest.mock import MagicMock
from unittest import TestCase
import skelebot as sb

class TestConfigConfig(TestCase):

    def setUp(self):
        args   = [sb.config.Param("env", None, "local", ["local", "dev", "prod"])]
        params = [sb.config.Param("mode", "m", "local", ["local", "dev", "prod"])]
        jobs = [sb.config.Job("run", "run.sh", "run the job", args, params, ["one", "two", "three"], "i")]
        deploy = [sb.config.Deploy("Artifactory", "repo.cars.com", "cml", "my-ds-proj")]
        artifacts = [sb.config.Artifact("model", "mymodel.RData", deploy)]
        kerberos = sb.config.Kerberos("sshookman", "sshookman.keytab", "krb5.conf")
        plugins = [sb.config.Plugin("blorb", {'one': '1', 'two': '2'})]
        commands = ["apt-get install vim", "apt-get install java"]
        deps = ["numpy", "scipy", "scikit-learn"]
        ignore = ["*.RData", "*.pkl", "*.csv"]
        copy = ["my-file:/srv/file", "other-file:/var/file"]
        ports = ["1127:8080", "1128:8081"]

        self.cfg = sb.config.Config("proj", "my proj", "0.1.0", "1", "sean", "me", "Python", kerberos, commands, deps, ignore, jobs, artifacts,
                                    copy, "False", plugins, ports=ports, primaryJob="run")

        def genFile(content, filepath):
            return content

        self.cfg.generateFile = MagicMock(side_effect=genFile)
        
    # Test that the YAML is built correctly with all params
    def test_getYamlAll(self):
        yaml = self.cfg.getYaml()
        expected = """name: proj
description: my proj
version: 0.1.0
skelebotVersion: 1
maintainer: sean
contact: me
language: Python
kerberos: 
  hdfsUser: sshookman
  keytab: sshookman.keytab
  krbConf: krb5.conf
ephemeral: False
commands: 
- apt-get install vim
- apt-get install java
dependencies: 
- numpy
- scipy
- scikit-learn
ignore: 
- '*.RData'
- '*.pkl'
- '*.csv'
plugins: 
- name: blorb
  config: 
    one: 1
    two: 2
jobs: 
- name: run
  source: run.sh
  mode: i
  help: run the job
  args: 
  - name: env
    default: local
    choices: 
    - local
    - dev
    - prod
  params: 
  - name: mode
    alt: m
    default: local
    choices: 
    - local
    - dev
    - prod
  ignore: 
  - one
  - two
  - three
primaryJob: run
artifacts: 
- name: model
  file: mymodel.RData
  deploy: 
  - type: Artifactory
    url: repo.cars.com
    repo: cml
    path: my-ds-proj
ports: 
- 1127:8080
- 1128:8081
copy: 
- my-file:/srv/file
- other-file:/var/file
jupyter: 
  port: 8888
  folder: .
"""
        self.maxDiff = None
        self.assertEqual(expected, yaml)

    # Test that the appropriate base image is returned
    def test_getBaseImage(self):
        cfg = self.cfg
        self.assertEqual("skelebot/python-krb", cfg.getBaseImage())

        cfg.language = "R"
        self.assertEqual("skelebot/r-krb", cfg.getBaseImage())

        cfg.kerberos = None
        self.assertEqual("skelebot/r-devtools", cfg.getBaseImage())

        cfg.language = "Python"
        self.assertEqual("skelebot/python-base", cfg.getBaseImage())

    # Test that the version is bumped by patch
    def test_bumpPatch(self):
        self.assertEqual("0.1.1", self.cfg.bumpPatch())

    # Test that the version is bumped by minor
    def test_bumpMinor(self):
        self.assertEqual("0.2.0", self.cfg.bumpMinor())

    # Test that the version is bumped by major
    def test_bumpMajor(self):
        self.assertEqual("1.0.0", self.cfg.bumpMajor())

    # Test that the README that is generated has the correct values from the config
    def test_generateREADME(self):
        readme = self.cfg.generateREADME()
        self.assertTrue("# proj" in readme)
        self.assertTrue("Version-0.1.0-brightgreen.svg" in readme)
        self.assertTrue("Language-Python-yellow.svg" in readme)
        self.assertTrue("my proj" in readme)
        self.assertTrue("Project Maintainer: sean (me)" in readme)

    # Test that the gitignore is generated without error and the basic ignores
    def test_generateGitignore(self):
        gitignore = self.cfg.generateGitignore()
        self.assertTrue("*.RData" in gitignore)
        self.assertTrue("*.pkl" in gitignore)
        self.assertTrue("*.csv" in gitignore)

if __name__ == '__main__':
    unittest.main()
