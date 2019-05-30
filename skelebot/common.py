import pkg_resources
import os

VERSION = pkg_resources.get_distribution("skelebot").version
DESCRIPTION = """
\033[1m{project}\033[0m
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version (project): {sbVersion}
Skelebot Version (installed): {version}
-----------------------------------"""
SKELEBOT_HOME = "~/.skelebot"
PLUGINS_HOME = "{home}/plugins".format(home=SKELEBOT_HOME)

EXTENSION_COMMAND = {"py":"python ", "R":"Rscript ", "sh":"./"}
IMAGE_VERSION = {
    "0.2.2": 0.1,
    "0.2.1": 0.1,
    "0.2.0": 0.1,
    "0.1.2": 0.1,
    "0.1.1": 0.1,
    "0.1.0": 0.1
}
LANGUAGE_IMAGE = {
    "Python": {
        "base": "skelebot/python-base:{version}",
        "krb": "skelebot/python-krb:{version}"
    },
    "R":{
        "base": "skelebot/r-devtools:{version}",
        "krb": "skelebot/r-krb:{version}"
    }
}

LANGUAGE_DEPENDENCIES = {
    "Python":["numpy", "pandas", "scipy", "scikit-learn"],
    "R":["data.table", "here", "stringr", "readr", "testthat", "yaml"]
}

EXT_COMMAND= {"py":"python ", "R":"Rscript ", "sh":"./"}
