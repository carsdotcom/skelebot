# Skelebot - Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.12] - [IN PROGRESS]
### Changed
- **Jupyter** | Updates base image for python and updates jupyter component to fix some bugs that prevented it from being used

## [0.2.11] - 2019-06-24
### Changed
- **Docker Build** | Instead of retruning the status code, it now throws an exception if an error occurs (exiting if not handled)

## [0.2.10] - 2019-06-21
### Changed
- **Base Images** | Allows for both base and krb images, custom images, and default (no language) images

### Removed
- **Base Image Versions** | Just going to default to :latest unless a need arises to properly version

## [0.2.9] - 2019-06-18
### Added
- **Job Help Messages** | Adds support for help messages on the arguments and parameters for Skelebot jobs

## [0.2.8] - 2019-06-18
### Changed
- **Job Params** | Now support a new value (isBoolean) that defaults to false, but when set to true allows params to be boolean flags

## [0.2.7] - 2019-06-17
### Changed
- **Docker Run** | Updated the docker run process to handle more volume mapping formats (absolute and home based paths)
- **Docker Images** | No longer using base images, instead always using the krb images to keep things simple

## [0.2.6] - 2019-06-06
### Changed
- **Scaffolder** | Fixed the bug where the wrong values were getting placed into the Config class

## [0.2.5] - 2019-06-05
### Changed
- **Docker** | Python execution in Docker passes the -u param to display output to console
- **Image Versions** | Now only a single hardcoded image version, not a dictionary

### Removed
- **SkelebotVersion** | Removed the skelebotVersion from the config object (skelebot.yaml) as it is unused now

## [0.2.4] - 2019-06-04
### Changed
- **Parser** | Updated conditional check on choices to handle empty list instead of None, updated parse_args to support unit tests
- **Parser Test** | Updated the test cases here to actually evaluate the args being parsed and ensure that having and not having choices works

## [0.2.3] - 2019-05-30
### Changed
- **Scaffolder** | No longer sets up the skelebot home and plugins folders if they are missing
- **Plugin Component** | Sets up the skelebot home and plugins folders if they are missing
- **Component Factory** | Don't attempt to load plugins if folder is missing (bugfix)
- **Scaffolding Test** | Removes checks for folder generation logic
- **Plugin Test** | Adds checks and mocks for folder generation logic

## [0.2.2] - 2019-05-30
### Added
- **VERSION** | The single source of truth for the project version

### Changed
- **README** | Replaced the example output section with one that is up-to-date
- **setup.py** | No longer reads the yaml (as that require pyyaml), instead is hardcoded and reads only from VERSION
- **version** | Everything now reads from the VERSION file to get the version, skelebot code checks it's own package version
- **skelebot.yaml** | Updated to reflect the new 0.2.0 structure and removes the old one
- **docs** | Updated to reflect any and all changes from 0.1.2 to 0.2.1
- **Example Project** | Updated with more functionality and tested against v0.2.1
- **Job Param Defaults** | Bug fixed where default param values were missing
- **Env Support** | Bug fixed in yaml loading of env override config

### Removed
- **requirement.txt** | Not needed

## [0.2.1] - 2019-05-28
### Changed
- **Parser** | Includes scaffolding parser for non-skelebot projects

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
