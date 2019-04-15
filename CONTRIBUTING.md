Contributing
---

If you would like to get involved and contribute to this project, please read
through this document first in order to understand our Code of Conduct,
Process Guidelines, and the general Scope of the project.

---

## Maintainers

 * Sean Shookman | Data Scientist | sshookman@cars.com

## Contributor Code of Conduct

As contributors and maintainers of this project, and in the interest of
fostering an open and welcoming community, we pledge to respect all people who
contribute through reporting issues, posting feature requests, updating
documentation, submitting pull requests or patches, and other activities.

We are committed to making participation in this project a harassment-free
experience for everyone, regardless of level of experience, gender, gender
identity and expression, sexual orientation, disability, personal appearance,
body size, race, ethnicity, age, religion, or nationality.

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery
* Personal attacks
* Trolling or insulting/derogatory comments
* Public or private harassment
* Publishing other's private information, such as physical or electronic
  addresses, without explicit permission
* Other unethical or unprofessional conduct

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

By adopting this Code of Conduct, project maintainers commit themselves to
fairly and consistently applying these principles to every aspect of managing
this project. Project maintainers who do not follow or enforce the Code of
Conduct may be permanently removed from the project team.

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting a project maintainer. All complaints will be reviewed
and investigated and will result in a response that is deemed necessary and
appropriate to the circumstances. Maintainers are obligated to maintain
confidentiality with regard to the reporter of an incident.


This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 1.3.0, available at https://www.contributor-covenant.org/version/1/3/0/code-of-conduct.html

[homepage]: https://www.contributor-covenant.org

## Guidelines for Contributing

### Read The Docs

A lot of the information about the project can be found in the README. Make sure you have gone
over the README as well as this CONTRIBUTING document before starting on any contributions to
the project.

### Announce Your Work

If there is a reported issue that you are trying to fix, comment that you intend to solve it,
and possibly discuss with the project maintainers the best approach before starting to code.
If you intend to add new functionality, announce exactly what you are working on in detail
after making sure that it is in the scope of the project defined below.

Letting others know what you are working on helps prevent contributors from stepping on each
others' toes, and helps the maintainers to plan and organize the project.

### Fork the Repo

When you are ready to start working, fork this repository where you can begin coding.

### Maintain Tests, Comments, and Docs

Ensure all existing test cases are passing and any new test cases have been added to cover the
functionality that you introduce in your code.

Make sure code is commented well so that others can understand it fairly quickly. There is no
need to write paragraphs of explanation, but high level descriptions for functions, large segments
of code, or complicated code is very helpful.

If you are adding new functionality or modifying existing functionality, make sure the documentation
is updated accordingly.

### Open a Pull Request

Once you have made your changes in your forked repository branch (and all tests are passing) you
can open a Pull Request to get your code reviewed by the maintainers. Iterate your changes as the
project maintainers comment on your code. Once the maintainers have agreed that the code is ready,
it will be merged into the master branch of this repository.

## Project Scope

The purpose of this project is to create a generic build tool for machine learning projects. The
concept is to bring all of the various project management tasks that are done for ml projects
under one roof: Skelebot.

A key concept of this project is simplicity. In order to make things easier for the end-user of
Skelebot, this project should at a minimum only require the skelebot.yaml file in the root of
their project code. Since the purpose is to bring project tasks into a single location, the
skelebot.yaml file should be that location. All project configuration should exist in this file.

### Key Tasks

 * Dependency Management
 * Job Execution
 * Project Versioning
 * Continuous Integration
 * Artifact Management

### Planned Features

 * Scaffolding TravisCI
> The option to construct the travis ci file through skelebot. In keeping with the core concept
  of the project, this should be generated through skelebot from configuration in the skelebot.yaml
 file using a skelebot command. NOTE: We may want to make this generic to other CI/CICD tools in the future.
 * Configurable Volume Mapping
> Allow the user to specify volume mapping in skelebot.yaml (similar to copy)
 * Environment Configurations
> Allow for multiple configurations of skelebot based on environment. This should be a specific section
  of the skelebot.yaml config where users can specify environment names and any overriding config underneath.
  Needs to expose an optional parameter (--env -e) to allow users to select the environment config that will
  overwrite the default config.
