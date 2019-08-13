[Home](../index.md) > [API](../api.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 1</div>

---

- [Common](common.md)
- Objects
  - **Component** -- The base object for Plugins to allow them to hook into the Skelebot Systems
  - [SkeleYaml](skeleyaml.md) -- The base object for any config Class that needs to be marshalled to/from YAML
- Execution
  - [Docker](docker.md) -- The Docker execution functions for building images and running containers
- Generators
  - [YAML](yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>Component Module</h1>

The component module holds the classes required for creating new components/plugins. This inclues
Activation Enum as well as the Abstract Component Class as itself.

---

<h2 align='center'>Activation (Enum)</h2>

<h3 align='left'>Import</h3>

```
from skelebot.objects.component import Activation
```

The Activation Enum is used to set the level at which a component or plugin becomes active and
available for use within the Skelebot System. By default a component will only be active at the
CONFIG level, meaning it will only be active when the specific configuration data for said
component is in the skelebot.yaml file.

<h3 align='left'>Constants</h3>

|  NAME   | VALUE |                        DESCRIPTION                          |
|---------|-------|-------------------------------------------------------------|
|   EMPTY |   1   | Activates when no project is present                        |
|  CONFIG |   2   | Activates only when config data is present in skelebot.yaml |
| PROJECT |   3   | Activates when skelebot.yaml file exists                    |
|  ALWAYS |   4   | Activates always                                            |

---

<h2 align='center'>Component (SkeleYaml)</h2>

<h3 align='left'>Import</h3>

```
from skelebot.objects.component import Component
```

Everything in the Component object is designed such that it can be overridden by the values and
function implementations of the child class.

The values for the attributes and the implementation of the methods within the Component class
itself merely support the default behavior of a component.

<h3 align='left'>Attributes</h3>

| NAME       | VALUE             | DESCRIPTION                                                                                               |
|------------|-------------------|-----------------------------------------------------------------------------------------------------------|
| activation | Activation.CONFIG | The default activation level for any component/plugin in Skelebot                                         |
| commands   | []                | The names of the Skelebot command(s) that are used to initiate the execute function of the given component|

<h3 align='left'>scaffold(self)</h3>

> return Component

```
The `scaffold` method offers a hook into the Skelebot Scaffolding System.

If you would like to prompt a user for input during the scaffolding process and have that input
stored as values in the config, you can place the prompt in this function.

This method must return an instance of the component object itself, ideally populated with the
values obtained in the prompts to the user.
```

<h3 align='left'>addParsers(self, subparsers)</h3>

> return subparsers

| PARAMETER  | TYPE | DESCRIPTION                                                                                               |
|------------|----------------------------------------------------------------------------|-------------------------------------|
| subparsers | [argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html) | The Skelebot subparser for commands |

```
The `addParsers` method allows for components to add their own parsers to the main subparser of
the SkeleParser System.

This allows for components to create their own commands that Skelebot can understand and then
execute via the `execute` method hook.

This method must return the subparsers object that was provided to it.
```

<h3 align='left'>appendDockerignore(self)</h3>

> return String

```
The `appenDockerignore` method allows for components to append any extra ignores they wish onto the
.dockerignore file generation process by simply returning a string of the ignore values.

The ignores must be formatted properly and separated by endline characters (`\n`).
```

<h3 align='left'>appendDockerfile(self)</h3>

> return String

```
The `appendDockerfile` method allows for components to add additional instructions into the
Dockerfile generation process by returning a formatted string of the instructions.
```

<h3 align='left'>execute(self, config, args)</h3>

> return None

| PARAMETER  | TYPE               | DESCRIPTION                                                            |
|------------|--------------------|------------------------------------------------------------------------|
| config     | Config             | The Config object of the current project's skelebot.yaml configuration |
| args       | argparse.Namespace | The args namespace that was parsed from the SkeleParser                |

```
The `execute` method is executed when the command passed to Skelebot matches one of the values in
the component's `commands` attribute list.

This must be setup to be accepted as a command via the `addParsers` method in order for Skelebot
to accept the new command.

This method can do anything you want and does not need to return a value. In order to execute
something in Docker, you should make use of the Docker functions in the Execution System.
```

<h3 align='left'>prependCommand(self, job, native)</h3>

> return String

| PARAMETER | TYPE    | DESCRIPTION                                                            |
|-----------|---------|------------------------------------------------------------------------|
| job       | Job     | Skelebot Job Object for the job that is going to be executed           |
| native    | Boolean | Determines whether the job will run on the native system, or in Docker |

```
This method allows for components to add extra commands before the job execution, whether it is
native or in Docker by returning a string of the prepended command.
```

<h3 align='left'>appendCommand(self, job, native)</h3>

> return String

| PARAMETER | TYPE    | DESCRIPTION                                                            |
|-----------|---------|------------------------------------------------------------------------|
| job       | Job     | Skelebot Job Object for the job that is going to be executed           |
| native    | Boolean | Determines whether the job will run on the native system, or in Docker |

```
This method allows for components to add extra commands before the job execution, whether it is
native or in Docker by returning a string of the appended command.
```

<h3 align='left'>addDockerRunParams(self)</h3>

> return String

```
This method allows for additional parameters to be tacked onto the Docker run process by returning
a string of the desired parameters.
```

---
