[Home](../index.md) > [API](../api.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 1</div>

---

- [Common](common.md)
- Objects
  - [Component](component.md) -- The base object for Plugins to allow them to hook into the Skelebot Systems
  - [SkeleYaml](skeleyaml.md) -- The base object for any config Class that needs to be marshalled to/from YAML
- Execution
  - [Docker](docker.md) -- The Docker execution functions for building images and running containers
- Generators
  - [YAML](yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - **Dockerfile** -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>Dockerfile Generator Module</h1>

The Dockerfile Generator provides the function for building the project Dockerfile based on the
Config data so that the Project's Docker Image can be constructed.

---

<h3 align='left'>Import</h3>

```
from skelebot.systems.generators import dockerfile
```

<h3 align='left'>buildDockerfile(config)</h3>

> return None

| PARAMETER | TYPE   | DESCRIPTION                                                                               |
|-----------|--------|-------------------------------------------------------------------------------------------|
| config    | Config | The Config object representing the project configuration to be utilized in the Dockerfile |

```
This function will utilize the data from the Config object to construct a fully functioning Dockerfile
for the project with dependencies installed.
```
