"""Common Global Variables"""

import pkg_resources

from colorama import Style

VERSION = pkg_resources.get_distribution("skelebot").version
DESCRIPTION = Style.BRIGHT + "{project}" + Style.RESET_ALL + """
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version: {version}
-----------------------------------"""
SKELEBOT_HOME = "~/.skelebot"
PLUGINS_HOME = "{home}/plugins".format(home=SKELEBOT_HOME)
PLUGINS_QUARANTINE = "{home}/plugins-quarantine".format(home=SKELEBOT_HOME)

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
    },
    "R+Python": {
        "base": "skelebot/r-base",
        "krb": "skelebot/r-krb"
        
    }
}
_all_deps: dict = {"Python":["numpy", "pandas", "scipy", "scikit-learn"],"R":["data.table", "here", "stringr", "readr", "testthat", "yaml"]}
LANGUAGE_DEPENDENCIES = {
    "Python": _all_deps["Python"],
    "R": _all_deps["R"],
    "R+Python": _all_deps,
}

EXT_COMMAND = {"py":"python -u ", "R":"Rscript ", "sh":"bash ", "None":""}
