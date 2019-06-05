from ...objects.config import Config
from ...objects.job import Job

import os

FILE_PATH = "{path}/README.md"

# Builds the README based on the config
def buildREADME(config):

    readme = """# {name}
![Version](https://img.shields.io/badge/Version-{version}-brightgreen.svg)
![Documentation](https://img.shields.io/badge/Documentation-UNLINKED-red.svg)

{description}

---

## Contact
Project Maintainer: {maintainer} ({contact})"""
    readme = readme.format(name=config.name, description=config.description, version=config.version, maintainer=config.maintainer, contact=config.contact)

    readmeFile = open(FILE_PATH.format(path=os.getcwd()), "w")
    readmeFile.write(readme)
    readmeFile.close()
