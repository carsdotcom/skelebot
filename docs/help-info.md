[Home](index.md)

---

# Help Info

The most important command in Skelebot is the help command. This command will provide you a high level overview of commands that can be run through Skelebot, as well as detailed information for running specific commands, and even project specific jobs.

```
> skelebot -h
```

If this command is executed from inside a folder that is not a Skelebot project, you will be met with a simple message stating that your only options from this particular directory are to scaffold a new project, or install a plugin.

```
usage: skelebot [-h] [-v] {scaffold,plugin} ...

Skelebot Version: 2.0.0

positional arguments:
  {scaffold,plugin}
    scaffold         Scaffold a new or existing project with Skelebot
    plugin           Install a plugin for skelebot from a local zip file

optional arguments:
  -h, --help         show this help message and exit
  -v, --version      Display the version number of Skelebot
```

If the help command is run from inside a Skelebot project, the output looks quite different. The scaffold option is no longer available, as it is not needed, and the rest of the Standard Tasks are now present. More details for each task can be obtained by running the desired command with `-h` appended.

There are also more optional arguments available for these tasks, which allows you to run tasks natively (not in Docker), in specific environments, as well as to skip the build process for Docker. These optional arguments exist for all Skelebot custom jobs and therefore the argument must be placed directly after the skelebot command and before the job name (ex: `skelebot -d train`).

NOTE: The Artifactory tasks (push and pull) will only be present if artifacts are configuring in the skelebot.yaml file of the project.

```
usage: skelebot [-h] [-v] [-e ENV] [-d HOST] [-s] [-n] [-c] [-V] {loadData,train,score,push,pull,jupyter,plugin,bump,prime,exec,publish,envs} ...

Iris Example
Example Skelebot Project
-----------------------------------
Version: 1.1.0
Environment: None
Skelebot Version: 2.0.0
-----------------------------------

positional arguments:
  {loadData,train,score,push,pull,jupyter,plugin,bump,prime,exec,publish,envs}
    loadData            Load the Iris Dataset and save it into the data folder for the train job to access (src/loadData.py)
    train               Use the data loaded in the loadData job to train the iris model (src/train.py)
    score               Use the model that was built in the train job to score new data against the iris model (src/score.py)
    push                Push an artifact to Artifactory
    pull                Pull an artifact from Artifactory
    jupyter             Spin up Jupyter in a Docker Container (port=8888, folder=.)
    plugin              Install a plugin for skelebot from a local zip file
    bump                Bump the skelebot.yaml project version
    prime               Generate Dockerfile and .dockerignore and build the docker image
    exec                Exec into the running Docker container
    publish             Publish your versioned Docker Image to the registry
    envs                Display the available environments for the project

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display the version number of Skelebot
  -e ENV, --env ENV     Specify the runtime environment configurations
  -d HOST, --docker-host HOST
                        Set the Docker Host on which the command will be executed
  -s, --skip-build      Skip the build process and attempt to use previous docker build
  -n, --native          Run natively instead of through Docker
  -c, --contact         Display the contact email of the Skelebot project
  -V, --verbose         Print all job commands to the screen just before execution
```

### Version Parameter
The version of Skelebot is printed in the help output, but sometimes that is the only thing you want to check. If you just want to see the currently installed Skelebot version, you can use the version parameter (`-v --version`) to do just that.

```
> skelebot --version
Skelebot v.2.0.0
```

### Contact Parameter
Each project specifies a contact email address. This contact email can be retrieved from the command line directly by using the contact parameter (`-c --contact`).

```
> skelebot --contact
me@my-email.com
```

---

<center><< <a href="installing.html">Installing</a>  |  <a href="scaffolding.html">Scaffolding</a> >></center>
