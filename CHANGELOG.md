# Skelebot - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - IN PROGRESS
### Added
- **VERSION** | The single source of truth for the project version

### Changed
- **README** | Replaced the example output section with one that is up-to-date
- **setup.py** | No longer reads the yaml (as that require pyyaml), instead is hardcoded and reads only from VERSION
- **version** | Everything now reads from the VERSION file to get the version, skelebot code checks it's own package version
- **skelebot.yaml** | Updated to reflect the new 0.2.0 structure and removes the old one
- **docs** | Updated to reflect any and all changes from 0.1.2 to 0.2.1
- **Example Project** | Updated with more functionality and tested against v0.2.1

### Removed
- **requirement.txt** | Not needed

## [0.2.0] - 2019-05-24
### Added
- **CHANGELOG** | The document you are reading right now.
- **Test Cases** | For the new architecture

### Changed
- **README** | Adds versioning section for calling out SemVer and referencing the CHANGELOG.md
- **YAML** | The skelebot.yaml configuration file has a new structure based on the new component architecture
- **Architecture** | Restructuring the entire codebase without altering functionality (every python file has been refactored)
  - **Components** | Provide functionality on top of Skelebot base functionality
    - **Artifactory** | Push and pull artifacts to/from Artifactory
    - **Bump** | Bump the version number inthe skelebot.yaml file
    - **Dexec** | Docker execute to gain bash access to the container
    - **Jupyter** | Spin up Jupyter notebooks for the project
    - **Kerberos** | Allow for Kerberos authentication to HDFS
    - **Plugins** | Allow for plugins to be installed from zip files
    - **Prime** | Prime the project by building the Docker Image
  - **Systems** | Provide hooks for components and plugins to inject logic into the Skelebot system
    - **Execution** | The actual running of tasks whether it's native or in Docker
    - **Generators** | File generators and interpreters
    - **Parsing** | Argument parsing for any and all skelebot commands
    - **Scaffolding** | The entire scaffolding process for new and existing projects

### Removed
- **Old Test Cases** | From the old architecture (lack-of-architecture)

## [0.1.2] - 2019-04-30
### Added
- **CODE_OF_CONDUCT.md** | Contributing Code of Conduct

### Changed
- **CONTRIBUTING.md** | Now links to CODE_OF_CONDUCT.md instead of having the content directly
- **README.md** | Now used a differenet link name for linking to the CONTRIBUTING doc

## [0.1.1] - 2019-04-30
### Changed
- **CONTRIBUTING.md** | Including links to GitHub pages docs
- **Feature request template** | Indicates what is optional and required

## [0.1.0] - 2019-04-15
### Added
- **Everything!** | Initial Commit of the Project
