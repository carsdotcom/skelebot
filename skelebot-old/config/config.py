import os
from .job import *
from .artifact import *
from .kerberos import *
from .plugin import *
from .jupyter import *
from .templates import *
from ..globals import IMAGE_VERSION_MAP

class Config(YamlClass):
    'Config object for skelebot projects'
    name = None
    description = None
    version = None
    skelebotVersion = None
    maintainer = None
    contact = None
    langauge = None
    kerberos = None
    ephemeral = None
    commands = None
    plugins = None
    dependencies = None
    ignore = None
    jobs = None
    primaryJob = None
    artifacts = None
    ports = None
    copy = None
    jupyter = None

    def __init__(self, name, description, version, skelebotVersion, maintainer, contact, language, kerberos, commands, dependencies, ignore, jobs, artifacts, copy, ephemeral, plugins, jupyter=Jupyter(), ports=None, primaryJob=None):
        self.name = name
        self.description = description
        self.version = version
        self.skelebotVersion = skelebotVersion
        self.maintainer = maintainer
        self.contact = contact
        self.language = language
        self.kerberos = kerberos
        self.ephemeral = ephemeral
        self.commands = commands
        self.dependencies = dependencies
        self.ignore = ignore
        self.jobs = jobs
        self.primaryJob = primaryJob
        self.artifacts = artifacts
        self.ports = ports
        self.copy = copy
        self.plugins = plugins
        self.jupyter = jupyter

    @classmethod
    def getOrderedAttrs(cls):
        return ["name", "description", "version", "skelebotVersion", "maintainer", "contact", "language",
                "kerberos", "ephemeral", "commands", "dependencies", "ignore", "plugins",
                "jobs", "primaryJob", "artifacts", "ports", "copy", "jupyter"]

    # TODO: Would be nice to have a better way to handle the loading of child objects
    @classmethod
    def load(cls, cfg):
        values = {}
        for attr in cls.getOrderedAttrs():
            if (attr in cfg):
                if (attr == "jobs"):
                    values[attr] = Job.loadList(cfg[attr])
                elif (attr == "artifacts"):
                    values[attr] = Artifact.loadList(cfg[attr])
                elif (attr == "kerberos"):
                    values[attr] = Kerberos.load(cfg[attr])
                elif (attr == "plugins"):
                    values[attr] = Plugin.loadList(cfg[attr])
                elif (attr == "jupyter"):
                    values[attr] = Jupyter.load(cfg[attr])
                else:
                    values[attr] = cfg[attr]
            else:
                values[attr] = None
        return cls(**values)

    def getBaseImage(self):
        languageImages = {
            "Python": {
                "base": "skelebot/python-base:{version}".format(version=IMAGE_VERSION_MAP[self.skelebotVersion]),
                "krb": "skelebot/python-krb:{version}".format(version=IMAGE_VERSION_MAP[self.skelebotVersion])
            },
            "R":{
                "base": "skelebot/r-devtools:{version}".format(version=IMAGE_VERSION_MAP[self.skelebotVersion]),
                "krb": "skelebot/r-krb:{version}".format(version=IMAGE_VERSION_MAP[self.skelebotVersion])
            }
        }

        krb = "krb" if self.kerberos != None else "base"
        return languageImages[self.language][krb]

    def bumpPatch(self):
        mmp = self.version.split(".")
        mmp[2] = str(int(mmp[2]) + 1)
        version = ".".join(mmp)
        self.version = version
        return version

    def bumpMinor(self):
       mmp = self.version.split(".")
       mmp[1] = str(int(mmp[1]) + 1)
       mmp[2] = "0"
       version = ".".join(mmp)
       self.version = version
       return version

    def bumpMajor(self):
       mmp = self.version.split(".")
       mmp[0] = str(int(mmp[0]) + 1)
       mmp[1] = "0"
       mmp[2] = "0"
       version = ".".join(mmp)
       self.version = version
       return version

    def generateYaml(self):
        self.generateFile(self.getYaml(), "skelebot.yaml")

    def generateREADME(self):
        languageColors = {"Python":"yellow", "R":"blue"}
        readmeText = readme.format(name=self.name, description=self.description, version=self.version,
                                language=self.language, languageColor=languageColors[self.language],
                                maintainer=self.maintainer, contact=self.contact)
        return self.generateFile(readmeText, "README.md")

    def generateGitignore(self):
        return self.generateFile(gitignore, ".gitignore")

    def generateFile(self, content, filePath):
        file = open(filePath, "w")
        file.write(content)
        file.close()
        return True
