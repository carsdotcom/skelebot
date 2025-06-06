# Skelebot - Changelog
Documenting All Changes to the Skelebot Project

---

## v2.3.0
#### Added
- **Python 3.12** | Add support for python 3.12.

---

## v2.2.0
#### Merged: 2025-05-13
#### Changed
- **CI/CD** | Make all images work in both Intel (amd64) and Apple (arm64) CPUs.
- **Base Images** | The `python-krb` base image is **deprecated** and will be removed in skelebot 3.0

---

## v2.1.2
#### Merged: 2025-02-06
#### Changed
- **CI/CD** | Set up a schedule to automatically update all base images twice a month
- **Base Images** | Security update: Apply OS-level updates and set `setuptools` minimum version to 70.0.0 for all base images

---

## v2.1.1
#### Released: 2025-01-25
#### Merged: 2025-01-25
#### Changed
- **Package Component** | Updated `package` component to delete destination path if it already exists before archiving the codebase.

---

## v2.1.0
#### Released: 2024-11-27
#### Merged: 2024-11-27
#### Added
- **Package Component** | Added `package` component to allow easy zipping of codebase

---

## v2.0.1
#### Merged: 2024-06-27
#### Changed
- **Base Images** | Added `git` to all the base images.
- **CI/CD** | Upload base images to Docker Hub via GitHub Action whenever there's an update.

---

## v2.0.0
#### Merged: 2024-06-06
#### Released: 2024-06-06
#### Changed
- **Dependencies** | All project dependencies, regardless of source (individual packages, local or remote files, requirements files, pyproject scripts) are now installed together in a single `pip install ...` command.
- **Build system** | Refactored build system to use a single `pyproject.toml` script. Switched build backend from `setuptools` to `hatchling`.

#### Removed
- **Config** | Removed now unnecessary `language` config variable. Existing projects may keep that variable and it will be ignored going forward.
- **Artifactory** | Removed old deprecated Artifactory component.
- **Python versions** | Support for python versions 3.6, 3.7, and 3.8, including base docker images, is **removed**.
- **R support** | All support for `R` and `R+Python` projects, including base docker images, is **removed**.

---

## v1.37.0
#### Merged: 2023-05-29
#### Released: 2024-05-29
#### Deprecated
- **Python versions** | Support for python versions 3.6, 3.7, and 3.8, including base docker images, is **deprecated** and will be removed in skelebot 2.0
- **R support** | All support for `R` and `R+Python` projects, including base docker images, is **deprecated** and will be removed in skelebot 2.0

#### Added
- **Python 3.11** | Adding support for Python 3.11.

---

## v1.36.1
#### Merged: 2023-06-21
#### Released: 2023-06-21
#### Changed
- **Artifactory** | Using the default aws profile should pass `None` to boto3 Session.

---

## v1.36.0
#### Merged: 2023-06-20
#### Released: 2023-06-20
#### Changed
- **Artifactory** | Added support for token and api key methods of Artifactory authentication. Also added support to read authentication credentials from AWS Secrets Manager.

---

## v1.35.0
#### Merged: 2023-06-12
#### Changed
- **Spaced Params** | Adding support parameters and arguments with spaces by wrapping them in single quotes

---

## v1.34.0
#### Merged: 2023-05-10
#### Released: 2023-05-10
#### Changed
- **Python 3.10** | Adding support for Python 3.10

---

## v1.33.6
#### Merged: 2022-11-09
#### Changed
- **Semver object** | Fix bug with version comparison and add dedicated unit tests.

---

## v1.33.5
#### Merged: 2022-10-17
#### Changed
- **Skelebot Main** | Full test coverage for skelebot `__init__`.
- **Scaffolding** | Fixed a bug in scaffolding where scaffolded dict-like components would raise an error in configs with no `components` defined. Also increase test coverge of this module to 100%.

---

## v1.33.4
#### Merged: 2022-09-23
#### Released: 2022-09-21
#### Changed
- **Scaffolding** | Fixed a bug in scaffolding where templates were not having components loaded in the config section

---

## v1.33.1
#### Merged: 2022-09-19
#### Released: 2022-09-19
#### Changed
- **S3Repo** | Fixed a bug in S3Repo where the artifact version was not being parsed properly in some cases

---

## v1.33.0
#### Merged: 2022-09-09
#### Added
- **Git Templates** | Added the ability to load templates from Git repos in scaffolding

---

## v1.32.0
#### Merged: 2022-08-24
#### Changed
- **Push Prefix** | Added the ability to push artifacts to S3 or Artifactory with prefix text

---

## v1.31.0
#### Merged: 2022-05-24
#### Released: 2022-05-24
#### Changed
- **Dependencies** | Added the ability for python dependencies to be specified and installed via a `pyproject.toml` file

---

## v1.30.1
#### Merged: 2022-05-24
#### Changed
- **CodeArtifact Dependencies** | Create libs folder if it doesn't already exist

---

## v1.30.0
#### Merged: 2022-05-04
#### Released: 2022-05-04
#### Changed
- **Docker Publish** | Docker Publish allows for omitting version and LATEST tags

---

## v1.29.0
#### Merged: 2022-05-02
#### Released: 2022-05-02
#### Changed
- **CodeArtifact Dependencies** | Adds an option to pull CodeArtifact Python packages into a libs folder for install during docker build

---

## v1.28.0
#### Merged: 2022-04-15
#### Released: 2022-04-15
#### Changed
- **In Memory Pull** | Allows S3Repo class to pull artifacts and return them directly in python

---

## v1.27.3
#### Merged: 2022-03-04
#### Released: 2022-03-04
#### Changed
- **S3 Repository** | Fixed bug preventing the profile attribute from being empty

---

## v1.27.2
#### Merged: 2022-01-12
#### Changed
- **Scaffolding** | Fixed minor bug in scaffolding output text

---

## v1.27.1
#### Merged: 2022-01-12
#### Released: 2022-01-12
#### Changed
- **Scaffolding** | Added templates design and option for Dash template in Python projects

---

## v1.26.0
#### Merged: 2022-01-05
#### Changed
- **Base Images** | Added jupyter-lab to all the base images (even the R base image!)
- **Jupyter Component** | Added the option to the Jupyter component to spin up lab instead of notebook

---

## v1.25.0
#### Merged: 2021-12-08
#### Released: 2021-12-08
#### Changed
- **Dependencies** | Added the ability to run docker with gpu

---

## v1.24.0
#### Merged: 2021-11-17
#### Released: 2021-11-17
#### Changed
- **Dependencies** | Added the ability for python dependencies to be specified and installed via a txt file such as `requirements.txt`

---

## v1.23.0
#### Merged: 2021-10-28
#### Changed
- **Execution** | Added global `--verbose` parameter that prints all job commands to the screen just before execution.

---

## v1.22.0
#### Merged: 2021-10-21
#### Changed
- **Job** | Added new `native` parameter for jobs to run ALWAYS or NEVER natively

---

## v1.21.8
#### Merged: 2021-10-19
#### Changed
- **Scaffolding** | Full test coverage for scaffold function.
- **Component** | Full test coverage for Component base class.

---

## v1.21.7
#### Merged: 2021-10-04
#### Released: 2021-10-14
#### Changed
- **Python-Base Image** | Add support for python 3.9 projects with skelebot base image.

---

## v1.21.6
#### Merged: 2021-06-10
#### Changed
- **R-aws Image** | Publishes update for R-aws image to fix some dependency issues in R related to rlang

---

## v1.21.5
#### Merged: 2021-03-15
#### Changed
- **Python-Base Image** | Pushed python 3.8 base image to Docker Hub and allows users to specify python version for projects in skelebot.yaml with pythonVersion parameter

---

## v1.21.4
#### Merged: 2021-01-29
#### Changed
- **Registry Component** | Allows for the global `--skip-build` parameter to properly skipping the Docker build step in the publish process

---

## v1.21.3
#### Merged: 2021-01-29
#### Added
- **Commands Documentation** | Added documentation for the image commands feature in Skelebot

---

## v1.21.2
#### Merged: 2021-01-29
#### Released: 2021-01-29
#### Changed
- **Docker** | Include AWS registry region and profile when authenticating using AWS cli V2.

---

## v1.21.1
#### Merged: 2020-10-29
#### Changed
- **R-Base Image** | Fixes the r-base image to include pip3 which was previously included by default

---

## v1.21.0
#### Merged: 2020-10-27
#### Changed
- **Environments** | Adds a new component for listing the available environments in a skelebot project

---

## v1.20.3
#### Merged: 2020-10-22
#### Changed
- **Dependencies** | Make all skelebot dependencies less strict and replace the source of the artifactory package.

---

## v1.20.2
#### Merged: 2020-10-12
#### Changed
- **Dockerfile Generator** | Allows user to specify protocol in python github dependencies

---

## v1.20.1
#### Merged: 2020-10-10
#### Changed
- **Registry Component** | Add remote execution support to skelebot publish command

---

## v1.20.0
#### Merged: 2020-10-09
#### Changed
- **Repository Component** | Artifacts have an optional singular field that can be used to specify artifacts that do not use any versioning

---

## v1.19.2
#### Merged: 2020-10-07
#### Changed
- **Jupyter Component** | Propagate the docker host command to jupyter component

---

## v1.19.1
#### Merged: 2020-10-07
#### Changed
- **R Base Images** | Fixes issues with now borken R base images that was preventing them from building

---

## v1.19.0
#### Merged: 2020-08-03
#### Added
- **Host Parameter** | Adds a global optional parameter to set the docker host
- **Global Host Field** | Adds a global optional config field to set the docker host
- **Job Host Field** | Adds a job-level optional config field to set the docker host
#### Changed
- **Docker Command Building** | Refactors the way in which Docker Commands are built

---

## v1.18.5
#### Merged: 2020-05-27
#### Changed
- **AWS Redshift Base Image** | Adds a base image with R, Redshift drivers, and AWS CLI

---

## v1.18.4
#### Merged: 2020-04-09
#### Changed
- **Dockerfile Generator** | Changes the way we parse the primary job with ENTRYPOINT execution

---

## v1.18.3
#### Merged: 2020-04-08
#### Changed
- **R Images** | Updates the R images to use 3.6.3 because the 3.5.0 image was running on an outdated ubuntu version

---

## v1.18.2
#### Merged: 2020-03-26
#### Released: 2020-03-26
#### Changed
- **Repository ALL Keyword** | Adds simple keyword in repository for pushing or pulling ALL artifacts at once

---

## v1.18.1
#### Merged: 2020-03-12
#### Changed
- **Artifactory BugFix** | issue with ArtifactoryPath.glob function fixed by avoiding using the function altogether

---

## v1.18.0
#### Merged: 2020-03-10
#### Released: 2020-03-10
#### Changed
- **Job Ports** | Adds ability to map ports at the job level, instead of just globally

---

## v1.17.0
#### Merged: 2020-03-09
#### Released: 2020-03-09
#### Changed
- **Timezone** | Adds config property for setting the timezone of the Docker Container

---

## v1.16.2
#### Merged: 2020-03-09
#### Changed
- **S3 Repository** | Adds support for bucket names with "/" characters for pathing

---

## v1.16.1
#### Merged: 2020-02-27
#### Released: 2020-03-02
#### Changed
- **Docker** | Add support for V2 of AWS cli authentication of ECR repos.

---

## v1.16.0
#### Merged: 2020-02-10
#### Changed
- **Dockerfile Generator** | Swap order of copy and global commands in dockerfile generation.

---

## v1.15.3
#### Merged: 2020-01-28
#### Released: 2020-01-29
#### Changed
- **Unit Tests** | Updates unit tests for Dockerfile generation to ensure all scenarios are covered

---

## v1.15.2
#### Merged: 2020-01-28
#### Changed
- **Command Builder** | Fixes bug to handle list parameters properly by propogating the values without the brackets or commas

---

## v1.15.1
#### Merged: 2020-01-23
#### Changed
- **Docker Execution** | Replace os.system calls with subprocess.call
- **Executor** | Replace os.system calls with subprocess.call

---

## v1.15.0
#### Merged: 2020-01-23
#### Changed
- **Jupyter** | allow mapping folders outside of project folder

---

## v1.14.0
#### Merged: 2020-01-17
#### Changed
- **Executor** | allow passing short-handed parameter name
---

## v1.13.0
#### Changed
- **Registry** | Added optional 'aws' config to the component to allow for ECR authentication and publishing
- **Docker** | Added login method for AWS to allow for authenticating with ECR via the AWS CLI

---

## v1.12.1
#### Merged: 2020-01-17
#### Changed
- **Executor** | Fail job execution when status code is not zero

---

## v1.12.0
#### Merged: 2020-01-15
#### Released: 2020-01-15
#### Changed
- **Dockerfile Generator** | Adds the ability to construct ENTRYPOINT based Dockerfiles depending on the primaryExe field
- **Docker Execution** | Adds the ability to properly override ENTRYPOINT when running commands against an image

#### Added
- **PrimaryExe** | New config field to set the execution method for the primary job for either CMD or ENTRYPOINT

---

## v1.11.0
#### Merged: 2020-01-10
#### Changed
- **Artifactory** | Deprecated this component in favor of the new Repostiory component
- **config** | The config will not load the Artifactory component if the Repository component is present in the yaml
- **GitHub Pages** | Updated to reflect the deprecation and the new component

#### Added
- **Repository** | New component for managing artifacts in Artifactory or S3

---

## v1.10.1
#### Merged: 2020-01-02
#### Released: 2020-01-02
#### Changed
- **Jupyter** | Run jupyter in docker `-it` mode.

---

## v1.10.0
#### Merged: 2020-01-02
#### Added
- **Dockerfile** | Add full support for pip version identifiers of dependencies.

---

## v1.9.2
#### Merged: 2019-11-27
#### Changed
- **Python Base Image** | Install basic compilers (+60MB) and update pip on python base image.
- **Python Kerberos Image** | Remove `build-essentials` since that is in the python base image.

---

## v1.9.1
#### Merged: 2019-11-20
#### Added
- **Publish Tags Parameter** | Added "tags" parameter to the publish command to allow for multiple custom tags to be used when publishing the image

---

## v1.9.0
#### Merged: 2019-11-15
#### Added
- **Latest Compatible Version** | Added logic to artifactory pull commands to allow for dynamic look-up of the latest compatible version of an artifact
- **Override Artifact** | Added an override parameter to the artifact component to allow for pull commands to write to the existing artifact file location

---

## v1.8.5
#### Merged: 2019-11-14
#### Added
- **Contact Param** | Added a global contact param for displaying the project's contact email

---

## v1.8.4
#### Merged: 2019-11-11
#### Released: 2019-11-12
#### Added
- **Plugin Quarantine** | Exception handling for plugins will quarantine any plugins that fail to load properly

---

## v1.8.3
#### Merged: 2019-11-09
#### Changed
- **Tests** | Mock skelebot's version number in tests.

---

## v1.8.2
#### Merged: 2019-11-08
#### Changed
- **Templates** | The templates (bug reports, feature requests, pull requests) were updated to make them simpler and faster to use

---

## v1.8.1
#### Merged: 2019-11-07
#### Added
- **Version Param** | Added a version param for displaying the version number of Skelebot

#### Changed
- **Global Params** | Updated all global params to be read into variables with `_global` at the end to avoid conflicts with sub-parser parameters
- **README Contributors** | Updated via contributors plugin to include the latest contributor
- **GitHub Pages** | Updated help info doc to include the `--version` parameter

---

## v1.8.0
#### Merged: 2019-11-07
#### Changed
- **Dependency management** | Updated scaffolding options to allow for both R+Python

---

## v1.7.6
#### Merged: 2019-11-06
#### Changed
- **CommandBuilder** | Fixed bug to allow kabob-case parameters to be built into the command properly

---

## v1.7.5
#### Merged: 2019-10-18
#### Changed
- **README** | Update the README to add contributors via new skelebot plugin
- **Contributors Plugin** | Adds config to the skelebot.yaml for the contributors plugin

---

## v1.7.4
#### Merged: 2019-10-17
#### Released: 2019-10-17
#### Changed
- **Install Python Dependencies** | Install python dependencies from git and files

---

## v1.7.3
#### Merged: 2019-10-17
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
