[Home](index.md)

---

# Jupyter

Skelebot provides a standard task to spin up Jupyer Notebooks (or Lab) inside Docker that contain all of the dependencies, code, and data you have in your project.

```
> skelebot jupyter
```

There are three configuration values that facilitate this task: port and folder are the primary of the two. These specify the port number on which the Docker container will map the running notebooks as well as the root folder that will be used in Jupyter.

The third is lab, which is a simple boolean value indicating whether or not to spin up jupyter lab instead of jupyter notebook.

All of these values are optional. By default the port will be set to 8888, the folder will simply be the root directory, and lab will default to False. The path to the folder will be relative to the root directory of the project.

```
...
components:
  jupyter:
    port: 1127
    folder: my-notebooks/r-notebooks
    lab: False
...
```

---

<center><< <a href="hdfs-kerberos.html">HDFS Kerberos</a>  |  <a href="plugins.html">Plugins</a> >></center>
