from .components.plugin import Plugin

VERSION = "0.2.0"
DESCRIPTION = """
\033[1m{project}\033[0m
{desc}
-----------------------------------
Version: {pVersion}
Environment: {env}
Skelebot Version (project): {sbVersion}
Skelebot Version (installed): {version}
-----------------------------------"""

COMPONENTS = [
    Plugin()
]
