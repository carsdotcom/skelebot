"""Common Global Variables"""

import pkg_resources

from colorama import Fore, Style

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
        "base": "skelebot/python-base:{pythonVersion}",
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
PYTHON_VERSIONS = ['3.6', '3.7', '3.8', '3.9']

TEMPLATES = {
    "Python": {
        "Dash": {
            "dirs": ["src/assets/"],
            "files": {
                "src/app.py": "templates/dash/app_py",
                "src/server.py": "templates/dash/server_py",
                "src/config.py": "templates/dash/config_py",
                "src/assets/style.css": "templates/dash/style_css"
            },
            "config": {
                "ephemeral": False,
                "language": "Python",
                "dependencies": ["dash~=2.0"],
                "ports": ["5000:5000"],
                "primaryExe": "CMD",
                "primaryJob": "run",
                "jobs": [{
                    "name": "run",
                    "source": "src/app.py",
                    "help": "Start the Dashboard"
                }]
            }
        },
        "Package": {
            "dirs": ["notebooks/", "test/", "jobs/"],
            "files": { },
            "config": {
                "ephemeral": False,
                "language": "Python",
                "dependencies": _all_deps["Python"]
            }
        },
        "Container": {
            "dirs": ["config/", "data/", "notebooks/", "queries/", "src/jobs/"],
            "files": { },
            "config": {
                "ephemeral": False,
                "language": "Python",
                "dependencies": _all_deps["Python"]
            }
        }
    },
    "R": {
        "Container": {
            "dirs": ["config/", "data/", "queries/", "src/jobs/"],
            "files": { },
            "config": {
                "ephemeral": False,
                "language": "R",
                "dependencies": _all_deps["R"]
            }
        }
    },
    "R+Python": {
        "Container": {
            "dirs": ["config/", "data/", "queries/", "src/jobs/"],
            "files": { },
            "config": {
                "ephemeral": False,
                "language": "R+Python",
                "dependencies": {
                    "Python": ["pandas"],
                    "R": _all_deps
                }
            }
        }
    }
}


EXT_COMMAND = {"py":"python -u ", "R":"Rscript ", "sh":"bash ", "None":""}

ERROR_HEADER = Fore.RED + "ERROR" + Style.RESET_ALL + " | "
ERROR = ERROR_HEADER + "{}"
SCHEMA_ERROR = ERROR_HEADER + "skelebot.yaml | {}"

WARN_HEADER = Fore.YELLOW + "WARN" + Style.RESET_ALL + " | "
DEPRECATION_WARNING = WARN_HEADER + "The {code} has been deprecated as of v{version}. {msg}"

INFO_HEADER = Fore.GREEN + "INFO" + Style.RESET_ALL + " | "
INFO = INFO_HEADER + "{}"
