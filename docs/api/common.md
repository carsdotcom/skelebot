[Home](../index.md) > [API](../api.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 2</div>

---

- **Common**
- Objects
  - [Component](component.md) -- The base object for Plugins to allow them to hook into the Skelebot Systems
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

<h1 align='center'>Common Module</h1>

<h3 align='left'>Import</h3>

```
import skelebot.common
```

The common module holds several constant values that are applicable to all aspects of Skelebot.

<h3 align='left'>Constants</h3>

|     NAME      |        VALUE          |         DESCRIPTION          |
|---------------|-----------------------|------------------------------|
| SKELEBOT_HOME | "~/.skelebot"         | Skelebot's home directory    |
| PLUGINS_HOME  | "~/.skelebot/plugins" | Plugin folder home directory |

---
