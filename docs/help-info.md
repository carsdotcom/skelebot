[Home](index.md)

---

# Help Info

The most important command in Skelebot is the help command. This command will porvide you a high level overview of commands that can be run through Skelebot, as well as detailed information for running specific commands, and even project specific jobs.

```
> skelebot -h
```

If this command is executed from inside a folder that is not a Skelebot project, you will be met with a simple message stating that your only options from this particular directory are to scaffold a new project, or install a plugin.

```
usage: skelebot [-h] {plugin,scaffold} ...

Skelebot Version: 1.0.0

positional arguments:
  {plugin,scaffold}
    plugin           Install a plugin for skelebot from a local zip file
    scaffold         Scaffold a new skelebot project from scratch

optional arguments:
  -h, --help         show this help message and exit
```

If the help command is run from inside a Skelebot project, the output looks quite different. The scaffold option is no longer available, as it is not needed, and the rest of the Standard Tasks are now present. More details for each task can be obtained by running the desired command with '-h' appended.

There are also more optional arguments available for these tasks, which allows you to run tasks natively (not in Docker), in specific environments, as well as to skip the build process for Docker. These optional arguments exist for all Skelebot custom jobs and therefore the argument must be placed directly after the skelebot command and before the job name (ex: 'skelebot -d train'). The standard tasks do not require Docker to execute, and therefore the optional parameters do not apply.

NOTE: The Artifactory tasks (push and pull) will only be present if artifacts are configuring in the skelebot.yaml file of the project.

```
usage: skelebot [-h] [-e ENV] [-s] [-d]
                {plugin,bump,prime,exec,jupyter,push,pull,loadData,train,score}
                ...

Iris Example
Example Skelebot Project
-----------------------------------
Version: 0.1.0
Environment: None
Skelebot Version (project): 1.0.0
Skelebot Version (installed): 1.0.0
-----------------------------------

positional arguments:
  {plugin,bump,prime,exec,jupyter,push,pull,loadData,train,score}
    plugin              Install a plugin for skelebot from a local zip file
    bump                Increment the version of the project
    prime               Prime skelebot with latest config
    exec                Start the Docker container and access it via bash
    jupyter             Start a Jupyter notebook inside of Docker
    push                Push an artifact to artifactory
    pull                Pull an artifact from artifactory
    loadData            Load the Iris Dataset and save it into the data folder for the train job to access (src/loadData.py)
    train               Use the data loaded in the loadData job to train the iris model (src/train.py)
    score               Use the model that was built in the train job to score new data against the iris model (src/score.py)

optional arguments:
  -h, --help            show this help message and exit
  -e ENV, --env ENV     Specify the runtime environment configurations
  -s, --skip-build      Skip the build process and attempt to use previous docker build
  -n, --native          Run natively instead of through Docker
```

---

<center><< <a href="installing.html">Installing</a>  |  <a href="scaffolding.html">Scaffolding</a> >></center>
