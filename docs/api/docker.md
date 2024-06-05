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
  - **Docker** -- The Docker execution functions for building images and running containers
- Generators
  - [YAML](yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>Docker Execution Module</h1>

The Docker Execution module allows for the building of Docker images based on the project config as
well as the running of the project's container with provided specifications and commands.

---

<h3 align='left'>Import</h3>

```
from skelebot.systems.execution import docker
```

<h3 align='left'>build(config)</h3>

> return int (status)

| PARAMETER | TYPE   | DESCRIPTION                                              |
|-----------|--------|----------------------------------------------------------|
| config    | Config | The Config object representing the project configuration |

```
The build function will construct (or reconstruct) the Dockerfile, the .dockerignore file, and the
Docker image itself based on the project config. It will then return the status of the build as an
int (0 = success) or throw an exception in the case of a failure.
```

<h3 align='left'>run(config, command, mode, ports, mappings, task)</h3>

> return int (status)

| PARAMETER  | TYPE   | DESCRIPTION                                                                                                 |
|------------|--------|-------------------------------------------------------------------------------------------------------------|
| config     | Config | The Config object representing the project configuration                                                    |
| command    | String | The Command that will be executed inside the container when it starts                                       |
| mode       | String | A String representing the mode in which Docker will run (i, it, d)                                          |
| ports      | List   | A list of colon separated port mapping strings (e.x. ["88:8888", "1127:1127"])                              |
| mappings   | List   | A list of colon separated volume mapping strings (e.x. ["local/dir:/app/dir"])                              |
| task       | name   | A string name for the task that is being executed to be appended to the image name to form a container name |

```
The run function will execute a Docker run command for the project's image, assuming one has already
been built. This function accepts numerous parameters to customize the manner in which the
container will be run, and returns the status code from the command itself.
```
