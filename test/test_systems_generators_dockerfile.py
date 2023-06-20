#try:
    #self.artifactory.execute(config, args)
    #self.fail("Exception Not Thrown")
#except RuntimeError as err:
    #self.assertEqual(str(err), "No Compatible Version Found")

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
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
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
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_entrypoint_exec(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.primaryExe = "ENTRYPOINT"

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base:3.6
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
ENTRYPOINT [\"bash\", \"build.sh\"]\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_entrypoint_path(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.primaryExe = "ENTRYPOINT"

        config.primaryJob = "test-entrypoint-path"
        job = sb.objects.job.Job(name="test-entrypoint-path", source="jobs/dummy.py")
        config.jobs.append(job)

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base:3.6
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
ENTRYPOINT ["python", "-u", "jobs/dummy.py"]\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_cmd_path(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.primaryExe = "CMD"

        config.primaryJob = "test-cmd-path"
        job = sb.objects.job.Job(name="test-cmd-path", source="jobs/dummy.py")
        config.jobs.append(job)

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base:3.6
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c "python -u jobs/dummy.py --log info"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('skelebot.systems.generators.dockerfile.call')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.makedirs')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_py_ca_file_error(self, mock_getcwd, mock_mkdir, mock_expanduser, mock_call):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_mkdir.return_value = 1
        mock_call.return_value = 1
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "Python"
        config.dependencies.append("ca_file:cars:12345:python-pkg:ml-lib:0.1.0:prod")

        try:
            sb.systems.generators.dockerfile.buildDockerfile(config)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), "Failed to Obtain CodeArtifact Package")

    @mock.patch('skelebot.systems.generators.dockerfile.call')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.makedirs')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_base_py(self, mock_getcwd, mock_mkdir, mock_expanduser, mock_call):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_mkdir.return_value = 1
        mock_call.return_value = 0
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "Python"
        config.dependencies.append("github:github.com/repo")
        config.dependencies.append("github:https://github.com/securerepo")
        config.dependencies.append("file:libs/proj")
        config.dependencies.append("ca_file:cars:12345:python-pkg:ml-lib:0.1.0:prod")
        config.dependencies.append("req:requirements.txt")
        config.dependencies.append("proj:pyproject.toml")
        config.dependencies.append("dtable=9.0")

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base:3.6
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
RUN ["pip", "install", "git+github.com/repo"]
RUN ["pip", "install", "git+https://github.com/securerepo"]
COPY libs/proj libs/proj
RUN ["pip", "install", "/app/libs/proj"]
COPY libs/ml_lib-0.1.0-py3-none-any.whl libs/ml_lib-0.1.0-py3-none-any.whl
RUN ["pip", "install", "/app/libs/ml_lib-0.1.0-py3-none-any.whl"]
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "/app/requirements.txt"]
RUN ["pip", "install", "requests", "numpy==1.22.0", "pandas~=1.1", "scikit-learn<=2.0.0 ; python_version<=\'3.6\'", "pytest ~= 6.2", "pytest-cov ~= 3.0", "fake-package == 1.2.3", "not-real"]
RUN ["pip", "install", "dtable==9.0"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        expectedCMD = "aws codeartifact get-package-version-asset --domain cars --domain-owner 12345 --repository python-pkg --package ml-lib --package-version 0.1.0 --profile prod --format pypi --asset ml_lib-0.1.0-py3-none-any.whl libs/ml_lib-0.1.0-py3-none-any.whl"

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        mock_mkdir.assert_called_with("{folder}/libs".format(folder=folderPath), exist_ok=True)
        mock_call.assert_called_with(expectedCMD, shell=True)
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_base_py_versions(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "Python"
        config.dependencies.append("dtable=9.0")
        config.dependencies.append("pandas==0.25")
        config.dependencies.append("numpy~=1.17")
        config.dependencies.append("requests>= 2.2, == 2.*")
        config.dependencies.append("scipy!= 1.3.*")

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/python-base:3.6
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
RUN ["pip", "install", "dtable==9.0"]
RUN ["pip", "install", "pandas==0.25"]
RUN ["pip", "install", "numpy~=1.17"]
RUN ["pip", "install", "requests>= 2.2, == 2.*"]
RUN ["pip", "install", "scipy!= 1.3.*"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
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
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
COPY conf /etc/krb5.conf
COPY tab /krb/auth.keytab
CMD /bin/bash -c \"/./krb/init.sh user && bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
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
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info && echo Duuuuuude\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
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
RUN ["pip", "install", "pyyaml"]
RUN ["pip", "install", "artifactory"]
RUN ["pip", "install", "argparse"]
RUN ["pip", "install", "coverage"]
RUN ["pip", "install", "pytest"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

    @mock.patch('skelebot.systems.generators.dockerfile.call')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.makedirs')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_R_py_ca_file_error(self, mock_getcwd, mock_mkdir, mock_expanduser, mock_call):
        folderPath = "{path}/test/files".format(path=self.path)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_mkdir.return_value = 1
        mock_call.return_value = -1
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "R+Python"
        config.dependencies = {
            "Python":[
                "numpy", "pandas",
                "github:github.com/repo", "github:https://github.com/securerepo",
                "file:libs/proj",
                "ca_file:cars:12345:python-pkg:ml-lib:0.1.0:prod",
                "dtable>=9.0", "dtable=9.0"
            ],
            "R":[
                "data.table", "here",
                "github:github.com/repo:cool-lib",
                "file:libs/proj:cool-proj",
                "dtable=9.0"
            ]
        }

        try:
            sb.systems.generators.dockerfile.buildDockerfile(config)
            self.fail("Exception Not Thrown")
        except Exception as exc:
            self.assertEqual(str(exc), "Failed to Obtain CodeArtifact Package")

    @mock.patch('skelebot.systems.generators.dockerfile.call')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.makedirs')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_R_plus_Python(self, mock_getcwd, mock_mkdir, mock_expanduser, mock_call):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        mock_mkdir.return_value = 1
        mock_call.return_value = 0
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "R+Python"
        config.dependencies = {
            "Python":[
                "numpy", "pandas",
                "github:github.com/repo", "github:https://github.com/securerepo",
                "file:libs/proj",
                "ca_file:cars:12345:python-pkg:ml-lib:0.1.0:prod",
                "dtable>=9.0", "dtable=9.0"
            ],
            "R":[
                "data.table", "here",
                "github:github.com/repo:cool-lib",
                "file:libs/proj:cool-proj",
                "dtable=9.0"
            ]
        }
        config.components.append(sb.components.kerberos.Kerberos("conf", "tab", "user"))

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/r-krb
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
RUN ["pip3", "install", "numpy"]
RUN ["pip3", "install", "pandas"]
RUN ["pip3", "install", "git+github.com/repo"]
RUN ["pip3", "install", "git+https://github.com/securerepo"]
COPY libs/proj libs/proj
RUN ["pip3", "install", "/app/libs/proj"]
COPY libs/ml_lib-0.1.0-py3-none-any.whl libs/ml_lib-0.1.0-py3-none-any.whl
RUN ["pip3", "install", "/app/libs/ml_lib-0.1.0-py3-none-any.whl"]
RUN ["pip3", "install", "dtable>=9.0"]
RUN ["pip3", "install", "dtable==9.0"]
RUN ["Rscript", "-e", "install.packages('data.table', repo='https://cloud.r-project.org'); library(data.table)"]
RUN ["Rscript", "-e", "install.packages('here', repo='https://cloud.r-project.org'); library(here)"]
RUN ["Rscript", "-e", "library(devtools); install_github('github.com/repo'); library(cool-lib)"]
COPY libs/proj libs/proj
RUN ["Rscript", "-e", "install.packages('/app/libs/proj', repos=NULL, type='source'); library(cool-proj)"]
RUN ["Rscript", "-e", "library(devtools); install_version('dtable', version='9.0', repos='http://cran.us.r-project.org'); library(dtable)"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
COPY conf /etc/krb5.conf
COPY tab /krb/auth.keytab
CMD /bin/bash -c "/./krb/init.sh user && bash build.sh --env local --log info\"\n"""
        sb.systems.generators.dockerfile.buildDockerfile(config)

        expectedCMD = "aws codeartifact get-package-version-asset --domain cars --domain-owner 12345 --repository python-pkg --package ml-lib --package-version 0.1.0 --profile prod --format pypi --asset ml_lib-0.1.0-py3-none-any.whl libs/ml_lib-0.1.0-py3-none-any.whl"

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)
        mock_mkdir.assert_called_with("{folder}/libs".format(folder=folderPath), exist_ok=True)
        mock_call.assert_called_with(expectedCMD, shell=True)

    @mock.patch('os.path.expanduser')
    @mock.patch('os.getcwd')
    def test_buildDockerfile_timezone(self, mock_getcwd, mock_expanduser):
        folderPath = "{path}/test/files".format(path=self.path)
        filePath = "{folder}/Dockerfile".format(folder=folderPath)

        mock_expanduser.return_value = "{path}/test/plugins".format(path=self.path)
        mock_getcwd.return_value = folderPath
        config = sb.systems.generators.yaml.loadConfig()
        config.language = "R"
        config.timezone = "America/Chicago"
        config.dependencies.append("github:github.com/repo:cool-lib")
        config.dependencies.append("file:libs/proj:cool-proj")
        config.dependencies.append("dtable=9.0")

        expectedDockerfile = """
# This Dockerfile was generated by Skelebot
# Editing this file manually is not advised as all changes will be overwritten by Skelebot

FROM skelebot/r-base
MAINTAINER Mega Man <megaman@cars.com>
WORKDIR /app
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ["Rscript", "-e", "install.packages('pyyaml', repo='https://cloud.r-project.org'); library(pyyaml)"]
RUN ["Rscript", "-e", "install.packages('artifactory', repo='https://cloud.r-project.org'); library(artifactory)"]
RUN ["Rscript", "-e", "install.packages('argparse', repo='https://cloud.r-project.org'); library(argparse)"]
RUN ["Rscript", "-e", "install.packages('coverage', repo='https://cloud.r-project.org'); library(coverage)"]
RUN ["Rscript", "-e", "install.packages('pytest', repo='https://cloud.r-project.org'); library(pytest)"]
RUN ["Rscript", "-e", "library(devtools); install_github('github.com/repo'); library(cool-lib)"]
COPY libs/proj libs/proj
RUN ["Rscript", "-e", "install.packages('/app/libs/proj', repos=NULL, type='source'); library(cool-proj)"]
RUN ["Rscript", "-e", "library(devtools); install_version('dtable', version='9.0', repos='http://cran.us.r-project.org'); library(dtable)"]
COPY . /app
RUN rm -rf build/
RUN rm -rf dist/
CMD /bin/bash -c \"bash build.sh --env local --log info\"\n"""

        sb.systems.generators.dockerfile.buildDockerfile(config)

        data = None
        with open(filePath, "r") as file:
            data = file.read()
        self.assertTrue(data is not None)
        self.assertEqual(data, expectedDockerfile)

if __name__ == '__main__':
    unittest.main()
