"""README File Generator"""

import os

FILE_PATH = "{path}/README.md"
README = """# {name}
![Version](https://img.shields.io/badge/Version-{version}-brightgreen.svg)
![Documentation](https://img.shields.io/badge/Documentation-UNLINKED-red.svg)

{description}

---

## Contact
Project Maintainer: {maintainer} ({contact})"""

# Builds the README based on the config
def buildREADME(config):
    """Build the README.md file based on values from the Config object"""

    name = config.name
    desc = config.description
    version = config.version
    maintainer = config.maintainer
    contact = config.contact

    readme = README.format(name=name, description=desc, version=version, maintainer=maintainer,
                           contact=contact)

    readmeFile = open(FILE_PATH.format(path=os.getcwd()), "w")
    readmeFile.write(readme)
    readmeFile.close()
