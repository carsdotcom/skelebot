[Home](index.md) > Jupyter

---

# Jupyter

Skelebot provides a standard task to spin up Jupyer Notebooks inside Docker that contain all of the dependencies, code, and data you have in your
project.

```
> skelebot notebooks
```

There are two configuration values that facilitate this task: port and folder. These specify the port number on which the Docker container will map the running notebooks as well as the root folder that will be used in Jupyter.

Both of these values are optional. By default the port will be set to 8888, and the folder will simply be the root directory of the project unless otherwise specified inside the skelebot.yaml. The path to the folder will be relative to the root directory of the project.

```
...
jupyter:
  port: 1127
  folder: my-notebooks/r-notebooks
...
```
