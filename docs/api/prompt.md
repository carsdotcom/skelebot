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
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - **Prompt** -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>Scaffolding Prompt Module</h1>

The prompt module provides a function to make CLI requests for information to the user during the
scaffolding process.

---

<h3 align='left'>Import</h3>

```
from skelebot.systems.scaffolding import prompt
```

<h3 align='left'>promptUser(message, options=None, boolean=False)</h3>

> return String

| PARAMETER | TYPE    | DESCRIPTION                                                                           |
|-----------|---------|---------------------------------------------------------------------------------------|
| message   | String  | The prompt message to be displayed via the command line to the user                   |
| options   | List    | The list of possible options that the user can enter for their response to the prompt |
| boolean   | Boolean | Whether or not the prompt should only accept a boolean response (y/N)                 |

```
This function can be used during a component's scaffolding process in order to get data from the
user to populate the attributes of a component. By default, the function will allow for any String
of text to be entered as a response. The options parameter allows for the prompt to lock the user's
response to a list of choices. The boolean parameter, if set to True, will ensure that the user's
response is either True or False. 
```
