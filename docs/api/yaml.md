[Home](../index.md) > [API](../api.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 2</div>

---

- [Common](common.md)
- Objects
  - [Component](component.md) -- The base object for Plugins to allow them to hook into the Skelebot Systems
  - [SkeleYaml](skeleyaml.md) -- The base object for any config Class that needs to be marshalled to/from YAML
- Execution
  - [Docker](docker.md) -- The Docker execution functions for building images and running containers
- Generators
  - **YAML** -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>YAML Generator Module</h1>

The YAML Generator provides functions for building the skelebot.yaml from a Config object and
loading a Config object from a skelebot.yaml file as well. It also provides functions for saving
and loading the VERSION file separately.

---

<h3 align='left'>Import</h3>

```
from skelebot.systems.generators import yaml
```

<h3 align='left'>loadConfig(env=None)</h3>

> return Config

| PARAMETER | TYPE   | DESCRIPTION                                                                |
|-----------|--------|----------------------------------------------------------------------------|
| env       | String | The String name of the selected Skelebot environment that should be loaded |

```
The loadConfig function will parse the skelebot.yaml file into a Config object along with the
version number from the VERSION file. If an environment name is specified with the 'env' parameter,
it will attempt to locate the corresponding override yaml file (skelebot-{env}.yaml) and use the
data inside to override the properties from the base file.
```

<h3 align='left'>saveConfig(config)</h3>

> return None

| PARAMETER  | TYPE   | DESCRIPTION                                                                    |
|------------|--------|--------------------------------------------------------------------------------|
| config     | Config | The Config object representing the project configuration to be saved to a file |

```
The saveConfig function will convert the Config object to a Dict based on each object's toDict
implementation and then persist the resulting Dict object to the skelebot.yaml file along with the
associated version number to the VERSION file.
```

<h3 align='left'>loadVersion()</h3>

> return String

```
This function will return the version number String from the VERSION file inside the project.
```

<h3 align='left'>loadVersion(version)</h3>

> return None

| PARAMETER  | TYPE   | DESCRIPTION                                                                              |
|------------|--------|------------------------------------------------------------------------------------------|
| version    | String | The string representation of the semantic version number to be saved to the VERSION file |

```
This function will persist the given version number String to the VERSION file for the project.
```
