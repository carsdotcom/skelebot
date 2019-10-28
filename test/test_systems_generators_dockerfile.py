import os
import unittest
from unittest import mock

import skelebot as sb

# Test plugin that says 'Duuuuuude' at the end of every command
class SayDude(sb.objects.component.Component):
    activation = sb.objects.component.Activation.ALWAYS

    def appendCommand(self, job, native):
        return "echo Duuuuuude"

class TestDockerfile(unittest.TestCase):
    path = ""

    # Get the path to the current working directory before we mock the function to do so
    def setUp(self):
        self.path = os.getcwd()
        self.maxDiff = None

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_no_language(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)
        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = None

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM ubuntu:18.04
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_base(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "R"
        config.dependencies.append("github:github.com/repo:cool-lib")
        config.dependencies.append("file:libs/proj:cool-proj")
        config.dependencies.append("dtable=9.0")

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/r-base
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["Rscript", "-e", "install.packages('pyyaml', repo='https://cloud.r-project.org'); library(pyyaml)"]
RUN ["Rscript", "-e", "install.packages('artifactory', repo='https://cloud.r-project.org'); library(artifactory)"]
RUN ["Rscript", "-e", "install.packages('argparse', repo='https://cloud.r-project.org'); library(argparse)"]
RUN ["Rscript", "-e", "install.packages('coverage', repo='https://cloud.r-project.org'); library(coverage)"]
RUN ["Rscript", "-e", "install.packages('pytest', repo='https://cloud.r-project.org'); library(pytest)"]
RUN ["Rscript", "-e", "library(devtools); install_github('github.com/repo'); library(cool-lib)"]
COPY libs/proj libs/proj
RUN ["Rscript", "-e", "install.packages('/app/libs/proj', repos=NULL, type='source'); library(cool-proj)"]
RUN ["Rscript", "-e", "library(devtools); install_version('dtable', version='9.0', repos='http://cran.us.r-project.org'); library(dtable)"]
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_base_py(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "Python"
        config.dependencies.append("github:github.com/repo")
        config.dependencies.append("file:libs/proj")
        config.dependencies.append("dtable=9.0")

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip3", "install", "pyyaml"]
RUN ["pip3", "install", "artifactory"]
RUN ["pip3", "install", "argparse"]
RUN ["pip3", "install", "coverage"]
RUN ["pip3", "install", "pytest"]
RUN ["pip3", "install", "git+github.com/repo"]
COPY libs/proj libs/proj
RUN ["pip3", "install", "/app/libs/proj"]
RUN ["pip3", "install", "dtable==9.0"]
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)
    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_krb(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "R"
        config.dependencies.append("github:github.com/repo:cool-lib")
        config.dependencies.append("file:libs/proj:cool-proj")
        config.dependencies.append("dtable=9.0")
        config.components.append(sb.components.kerberos.Kerberos("conf", "tab", "user"))

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/r-krb
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["Rscript", "-e", "install.packages('pyyaml', repo='https://cloud.r-project.org'); library(pyyaml)"]
RUN ["Rscript", "-e", "install.packages('artifactory', repo='https://cloud.r-project.org'); library(artifactory)"]
RUN ["Rscript", "-e", "install.packages('argparse', repo='https://cloud.r-project.org'); library(argparse)"]
RUN ["Rscript", "-e", "install.packages('coverage', repo='https://cloud.r-project.org'); library(coverage)"]
RUN ["Rscript", "-e", "install.packages('pytest', repo='https://cloud.r-project.org'); library(pytest)"]
RUN ["Rscript", "-e", "library(devtools); install_github('github.com/repo'); library(cool-lib)"]
COPY libs/proj libs/proj
RUN ["Rscript", "-e", "install.packages('/app/libs/proj', repos=NULL, type='source'); library(cool-proj)"]
RUN ["Rscript", "-e", "library(devtools); install_version('dtable', version='9.0', repos='http://cran.us.r-project.org'); library(dtable)"]
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
COPY conf /etc/krb5.conf
COPY tab /krb/auth.keytab
CMD /bin/bash -c \"/./krb/init.sh user && bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_no_command(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        # No custom docker run command
        config.commands = []
        config.language = None

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM ubuntu:18.04
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_append_command(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = None
        config.components.append(SayDude())

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM ubuntu:18.04
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info && echo Duuuuuude\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_custom(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.baseImage = "whatever:uwant"

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM whatever:uwant
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip3", "install", "pyyaml"]
RUN ["pip3", "install", "artifactory"]
RUN ["pip3", "install", "argparse"]
RUN ["pip3", "install", "coverage"]
RUN ["pip3", "install", "pytest"]
RUN rm -rf build/
RUN rm -rf dist/
COPY . /app
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        print(data)
        self.assertEqual(data, expectedDockerfile)

if __name__ == '__main__':
    unittest.main()
