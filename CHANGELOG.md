# Skelebot - Changelog
Documenting All Changes to the Skelebot Project

---

## v1.7.3
#### Changed
- **CI/CD** | Changed PyPI GitHub Action to use token instead of password

---

## v1.7.2
#### Merged: 2019-10-16
#### Changed
- **Main Get Env** | Fixed bug in the get_env() function in skelebot.py to handle base skelebot args/parameters

---

## v1.7.1
#### Merged: 2019-10-09
#### Changed
- **Tests** | Increase test coverage to 99%.

---

## v1.7.0
#### Merged: 2019-10-09
#### Changed
- **Docker build** | Append env to image name if present.

---

## v1.6.4
#### Merged: 2019-10-05
#### Changed
- **Dependency management** | Added requirements.txt as single source of truth for dependencies.

---

## v1.6.3
#### Merged: 2019-10-02
#### Changed
- **CI/CD** | Update PyPI workflow to trigger on prereleases only.

---

## v1.6.2
#### Merged: 2019-10-02
#### Released: 2019-10-02
#### Changed
- **CI/CD** | Upload skelebot releases to PyPI via GitHub Action.

---

## v1.6.1
#### Merged: 2019-10-02
#### Changed
- **README** | Properly centering the project title logo image with GitHub specific markdown html

---

## v1.6.0
#### Merged: 2019-10-02
#### Added
- **Global commands** | Adds optional docker RUN commands property to root config that are executed after dependencies are installed

---

## v1.5.3
#### Merged: 2019-10-02
#### Released: 2019-10-02
#### Changed
- **Dependency Versions** | Explicitly setting versions for coverage and pytest dependencies

---

## v1.5.2
#### Merged: 2019-10-01
#### Added
- **Common** | Use colorama for cross-platform colored output
- **Skelebot Main** | Use colorama for cross-platform highlighted output

---

## v1.5.1
#### Merged: 2019-10-01
#### Changed
- **Skelebot Main** | Fixes bug where the parsing of the skelebot --env param could conflict with params on jobs

---

## v1.5.0
#### Merged: 2019-10-01
#### Added
- **Registry Component** | Adds a new component to store registry info for publishing images
- **Docker Login** | Adds docker login function to login to a given registry host
- **Docker Push** | Adds docker push function to tag and push images to the specified registry

---

## v1.4.0
#### Merged: 2019-10-01
#### Changed
- **Jobs** | Updated the jobs to execute the commands given in source as it is, along with support for execution of scripts

---

## v1.3.4
#### Merged: 2019-09-27
#### Changed
- **Logo** | Updated the logo with Skelly's new prompt-style robot eye and removed the transparency
- **README** | Updated Logo in README and Centered the Title and Subtitle, and updates description
- **Docs** | Updated GitHub Pages with better description (project development instead of project management)

---

## v1.3.3
#### Merged: 2019-09-12
#### Added
- **AWS Base Image** | Adds a base image with R and AWS CLI that is not used by default in Skelebot yet

---

## v1.3.2
#### Merged: 2019-09-09
#### Added
- **Environment Errors** | Returns an error message when attempting to use an env that does not exist

---

## v1.3.1
#### Merged: 2019-09-06
#### Added
- **Python Base Lib** | Adds a library into the python base image that is needed for certain python packages

---

## v1.3.0
#### Merged: 2019-09-05
#### Released: 2019-09-05
#### Added
- **Prime Output** | Add a param to prime component to allow for saving the Docker image as a file

---

## v1.2.1
#### Merged: 2019-09-04
#### Released: 2019-09-05
#### Added
- **Tests** | Added more test cases to cover important edge cases that were missed

---

## v1.2.0
#### Merged: 2019-08-22
#### Added
- **Primary Job** | Added the ability for primary job to accept component hooks and use default params

---

## v1.1.2
#### Merged: 2019-08-21
#### Changed
- **Docker Run** | Updated the docker run process to operate properly on Windows machines

---

## v1.1.1
#### Merged: 2019-08-15
#### Released: 2019-08-19
#### Changed
- **Artifcatory Component** | Fixes a major bug where auth was not being utilized in path checking

---

## v1.1.0
#### Merged: 2019-08-14
#### Added
- **SkeleYaml | Validate** | Adds schema based validation for SkeleYaml objects and exception handling output

---

## v1.0.3
#### Merged: 2019-08-07
#### Changed
- **Bash Exec** | Bash scripts are now executed using `bash {script}` instead of `./{script}` for better stability

---

## v1.0.2
#### Merged: 2019-08-06
#### Changed
- **Lint** | Went through the ENTIRE codebase and made non-breaking refactors and additions for linting purposes
- **README** | Adds badge for Codacy, License, and PyPi Release version

---

## v1.0.1
#### Merged: 2019-08-05
#### Released: 2019-08-05
#### Changed
- **Artifactory Component** | Fixes bug where the `--user` and `--token` params were not being read in properly

---

## v1.0.0
#### Merged: 2019-08-01
#### Released: 2019-08-01
#### Added
- **PyPi Package** | Adds the package to PyPi so it can be installed via pip

#### Changed
- **Documenation** | Docs updated to reflect the new install process via pip

---

## v0.3.1
#### Merged: 2019-08-01
#### Added
- **CodeCov** | Adds config in CircleCI to upload coverage report to CodeCov
- **README Badge** | Adds CodeCov README badge

---

## v0.3.0
#### Merged: 2019-08-01
#### Changed
- **Yaml Generator** | Now saves and loads the VERSION file separately - a VERSION file is now needed for proper skelebot versioning
- **Bump Component** | Now only saves to the VERSION file and does not update the config yaml
- **Docs** | Updated to reflect the new change in the way versions are handled in Skelebot

---

## v0.2.22
#### Merged: 2019-08-01
#### Changed
- **SkeleParser** | Removes the default value for boolean params in jobs as it is not needed
- **CommandBuilder** | Updated to only pass boolean params to scripts if the value is present and True

---

## v0.2.21
#### Merged: 2019-07-30
#### Added
- **Job Chaining** | Adds ability to chain jobs together using the '+' character to separate the commands

---

## v0.2.20
#### Merged: 2019-07-29
#### Changed
- **Exec Component** | Fixes a minor bug where the image name was being duplicated in the container name

---


## v0.2.19
#### Merged: 2019-07-25
#### Changed
- **Top-Level Params** | Fixes a bug where only the default would work for top-level parameters

---

## v0.2.18
#### Merged: 2019-07-24
#### Changed
- **Primary Jobs** | Fixes bug to allow primary jobs to execute as exepcted without specifying a command in the docker run process

---

## v0.2.17
#### Merged: 2019-07-16
#### Changed
- **Env Configs** | Fixes bug to allow env config to add properties that are not present in the default (parent) config

---

## v0.2.16
#### Merged: 2019-07-12
#### Added
- **accepts** | Adds 'accept' field on params to specify lists or boolean params

#### Changed
- **Params** | The Param object has been split and a new object (Arg) is now used for job arguments

#### Removed
- **isBoolean** | Removes the 'isBoolean' field on params in favor of the 'accepts' field

---

## v0.2.15
#### Merged: 2019-07-09
#### Added
- **Global Params** | Adds global params list to root of config to allow parameters defined once applied to each job

---

## v0.2.14
#### Merged: 2019-06-28
#### Changed
- **Exec** | The exec command now accepts a flag (-m --map) to allow volume maps of the working directory onto the container's /app folder so changes in exec can be persisted

---

## v0.2.13
#### Merged: 2019-06-28
#### Changed
- **r-base** | Updates the r-base image to add an install for gfortran compiler that some packages require
- **CHANGELOG** | Updating the structure of the doc a bit

---

## v0.2.12
#### Merged: 2019-06-25
#### Changed
- **Jupyter** | Updates base image for python and updates jupyter component to fix some bugs that prevented it from being used

---

## v0.2.11
#### Merged: 2019-06-24
#### Changed
- **Docker Build** | Instead of retruning the status code, it now throws an exception if an error occurs (exiting if not handled)

---

## v0.2.10
#### Merged: 2019-06-21
#### Changed
- **Base Images** | Allows for both base and krb images, custom images, and default (no language) images

#### Removed
- **Base Image Versions** | Just going to default to :latest unless a need arises to properly version

---

## v0.2.9
#### Merged: 2019-06-18
#### Added
- **Job Help Messages** | Adds support for help messages on the arguments and parameters for Skelebot jobs

---

## v0.2.8
#### Merged: 2019-06-18
#### Changed
- **Job Params** | Now support a new value (isBoolean) that defaults to false, but when set to true allows params to be boolean flags

---

## v0.2.7
#### Merged: 2019-06-17
#### Changed
- **Docker Run** | Updated the docker run process to handle more volume mapping formats (absolute and home based paths)
- **Docker Images** | No longer using base images, instead always using the krb images to keep things simple

---

## v0.2.6
#### Merged: 2019-06-06
#### Changed
- **Scaffolder** | Fixed the bug where the wrong values were getting placed into the Config class

---

## v0.2.5
#### Merged: 2019-06-05
#### Changed
- **Docker** | Python execution in Docker passes the -u param to display output to console
- **Image Versions** | Now only a single hardcoded image version, not a dictionary

#### Removed
- **SkelebotVersion** | Removed the skelebotVersion from the config object (skelebot.yaml) as it is unused now

---

## v0.2.4
#### Merged: 2019-06-04
#### Changed
- **Parser** | Updated conditional check on choices to handle empty list instead of None, updated parse_args to support unit tests
- **Parser Test** | Updated the test cases here to actually evaluate the args being parsed and ensure that having and not having choices works

---

## v0.2.3
#### Merged: 2019-05-30
#### Changed
- **Scaffolder** | No longer sets up the skelebot home and plugins folders if they are missing
- **Plugin Component** | Sets up the skelebot home and plugins folders if they are missing
- **Component Factory** | Don't attempt to load plugins if folder is missing (bugfix)
- **Scaffolding Test** | Removes checks for folder generation logic
- **Plugin Test** | Adds checks and mocks for folder generation logic

---

## v0.2.2
#### Merged: 2019-05-30
#### Added
- **VERSION** | The single source of truth for the project version

#### Changed
- **README** | Replaced the example output section with one that is up-to-date
- **setup.py** | No longer reads the yaml (as that require pyyaml), instead is hardcoded and reads only from VERSION
- **version** | Everything now reads from the VERSION file to get the version, skelebot code checks it's own package version
- **skelebot.yaml** | Updated to reflect the new 0.2.0 structure and removes the old one
- **docs** | Updated to reflect any and all changes from 0.1.2 to 0.2.1
- **Example Project** | Updated with more functionality and tested against v0.2.1
- **Job Param Defaults** | Bug fixed where default param values were missing
- **Env Support** | Bug fixed in yaml loading of env override config

#### Removed
- **requirement.txt** | Not needed

---

## v0.2.1
#### Merged: 2019-05-28
#### Changed
- **Parser** | Includes scaffolding parser for non-skelebot projects

---

## v0.2.0
#### Merged: 2019-05-24
#### Added
- **CHANGELOG** | The document you are reading right now.
- **Test Cases** | For the new architecture

#### Changed
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

#### Removed
- **Old Test Cases** | From the old architecture (lack-of-architecture)

---

## v0.1.2
#### Merged: 2019-04-30
#### Added
- **CODE_OF_CONDUCT.md** | Contributing Code of Conduct

#### Changed
- **CONTRIBUTING.md** | Now links to CODE_OF_CONDUCT.md instead of having the content directly
- **README.md** | Now used a differenet link name for linking to the CONTRIBUTING doc

---

## v0.1.1
#### Merged: 2019-04-30
#### Changed
- **CONTRIBUTING.md** | Including links to GitHub pages docs
- **Feature request template** | Indicates what is optional and required

---

## v0.1.0
#### Merged: 2019-04-15
#### Added
- **Everything!** | Initial Commit of the Project

---
