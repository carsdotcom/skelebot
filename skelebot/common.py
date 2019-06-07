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

IMAGE_VERSION = 0.1
LANGUAGE_IMAGE = {
    "Python": "skelebot/python-krb:{version}",
    "R": "skelebot/r-krb:{version}"
}

LANGUAGE_DEPENDENCIES = {
    "Python":["numpy", "pandas", "scipy", "scikit-learn"],
    "R":["data.table", "here", "stringr", "readr", "testthat", "yaml"]
}

EXT_COMMAND= {"py":"python -u ", "R":"Rscript ", "sh":"./"}
