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
  - [YAML](yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - **Dockerignore** -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>Dockerignore Generator Module</h1>

The Dockerignore Generator provides the function for building the project .dockerignore based on the
Config data so that only required files and folders are included in the Docker build process.

---

<h3 align='left'>Import</h3>

```
from skelebot.systems.generators import dockerignore
```

<h3 align='left'>buildDockerignore(config)</h3>

> return None

| PARAMETER | TYPE   | DESCRIPTION                                                                                  |
|-----------|--------|----------------------------------------------------------------------------------------------|
| config    | Config | The Config object representing the project configuration to be utilized in the .dockerignore |

```
This function will utilize the ignores list from the Config object to construct a fully functioning
.dockerignore file for the project in order to omit specific files and folders and reduce the
amount of data inside the build context during the Docker build process.
```
