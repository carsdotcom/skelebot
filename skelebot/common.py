"""Common Global Variables"""

from importlib import metadata

from colorama import Fore, Style

VERSION = metadata.version("skelebot")
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
    "base": "skelebot/python-base:{pythonVersion}",
    "krb": "skelebot/python-krb"
}

PYTHON_VERSIONS = ['3.9', '3.10', '3.11', '3.12']
DEPRECATED_VERSIONS = []

TEMPLATE_PATH = "templates/{name}"
TEMPLATES =  {
    "Default": "python",
    "Dash": "python_dash",
    "Git": "git"
}

EXT_COMMAND = {"py":"python -u ", "R":"Rscript ", "sh":"bash ", "None":""}

ERROR_HEADER = Fore.RED + "ERROR" + Style.RESET_ALL + " | "
ERROR = ERROR_HEADER + "{}"
SCHEMA_ERROR = ERROR_HEADER + "skelebot.yaml | {}"

WARN_HEADER = Fore.YELLOW + "WARN" + Style.RESET_ALL + " | "
DEPRECATION_WARNING = WARN_HEADER + "The {code} has been deprecated as of v{version}. {msg}"

INFO_HEADER = Fore.GREEN + "INFO" + Style.RESET_ALL + " | "
INFO = INFO_HEADER + "{}"
