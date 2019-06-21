import pkg_resources
import os

VERSION = pkg_resources.get_distribution("skelebot").version
DESCRIPTION = """
\033[1m{project}\033[0m
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version: {version}
-----------------------------------"""
SKELEBOT_HOME = "~/.skelebot"
PLUGINS_HOME = "{home}/plugins".format(home=SKELEBOT_HOME)

LANGUAGE_IMAGE = {
    "NA": {
        "base": "ubuntu:18.04",
        "krb": "ubuntu:18.04"
    },
    "Python": {
        "base": "skelebot/python-base",
        "krb": "skelebot/python-krb"
    },
    "R": {
        "base": "skelebot/r-base",
        "krb": "skelebot/r-krb"
    }
}

LANGUAGE_DEPENDENCIES = {
    "Python":["numpy", "pandas", "scipy", "scikit-learn"],
    "R":["data.table", "here", "stringr", "readr", "testthat", "yaml"]
}

EXT_COMMAND= {"py":"python -u ", "R":"Rscript ", "sh":"./"}
