Contributing
---

If you would like to get involved and contribute to this project, please read
through the [Code of Conduct](CODE_OF_CONDUCT.md) first. Then, read through 
this document to understand Process Guidelines, and the general Scope of the project.

---

## Maintainers

 * Sean Shookman | Data Scientist | sshookman@cars.com

## Project Scope

The purpose of this project is to create a generic build tool for machine learning projects. The
concept is to bring all of the various project management tasks that are done for machine learning projects
under one roof: Skelebot.

A key concept of this project is simplicity. Since the purpose is to bring project tasks into a
single location, the skelebot.yaml file should be that location. All project configuration should
exist in this file.

When considering new features for skelebot, the trick is to figure out where it belongs. Features
can be incorporated into Skelebot in 3 different ways.

### System Features

System features make up the core functionality of Skelebot. Other features of Skelebot (components)
are built on top of them. A good example would be the Execution System which handles all execution
of commands, both Docker and native.

Systems are also defined by the hooks that they provide for components to inject data or functionality
into their normal process. These hooks act as a well-defined, well-regulated, gateway for components to
augment the core functionality of Skelebot.

A new feature should be only be incorporated as a System (or into an existing System) if it is
a foundational part of what makes Skelebot function.

### Component Features

Components simply hook into the existing Skelebot Systems to add new functionality on top of
the existing structure. Components are self-contained, specific, purpose focused features that add
a distinct new ability into Skelebot's arsenal.

These features will be a part of every Skelebot installation, so it is important that only generally
applicable features be included as components. Anything that has such a specific purpose as to be
practically unused in the majority of projects, should not be a component in Skelebot.

### Plugin Features

Finally, anything that does not fit into Skelebot as a System or as a Component should be
a Plugin. A Plugin is just a Component that stands on it's own and can be optionally
installed into any Skelebot application. Plugins hook into Skelebot's Systems in the exact same way
as Components.

## Guidelines for Contributing

### Read The Docs

A lot of the information about the project can be found in the [README](README.md) and the
[GitHub Pages](https://carsdotcom.github.io/skelebot/). Make sure you have gone over the
documentation before starting on any contributions to the project.

### Announce Your Work

All issues (bugs, features, and tasks) are tracked in GitHub [Issues](https://github.com/carsdotcom/skelebot/issues).

If you would like to request a new feature or raise a bug, you can use the appropriate issues
templates to do so. Before opening a feature request, be sure it fits into the 'Project Scope'
that is defined above.

If there is a reported issue that you would like to work on, comment on the issue directly
and discuss with the project maintainers the best approach before starting to code.

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

Once you have made your changes in your forked repository (and all tests are passing) you
can open a Pull Request to get your code reviewed by the maintainers. Iterate your changes as the
project maintainers comment on your code. Once the maintainers have agreed that the code is ready,
it will be merged into the master branch of this repository and become a part of Skelebot. Yay!
