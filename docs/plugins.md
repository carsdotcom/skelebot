[Home](index.md)

---

# Plugins

The purpose of a Skelebot plugin is to add some extra functionality into Skelebot that doesn't already exist. This can be anything, but usually it is more useful when the plugin is trying to accomplish a specific task that most projects would not have a use for. If the functionality you are trying to implement seems general to all machine learning projects, consider instead contributing it directly to Skelebot instead of making a plugin.

### Install
Installing new plugins is very simple, all that is needed is a zip file of plugin code structured properly and named after the name of the plugin itself.

```
> skelebot plugin testPlugin.zip
```

Once installed the plugin can be used immediately. Some plugins required config in the skelebot.yaml to be present in order to work, as demonstrated in the example below, so be sure to consult any documentation for the plugin to find out how to properly make use of it. Since scaffolding only applies to new Skelebot projects, the details in the config file may need to be entered manually for existing projects.

### Structure

A Skelebot plugin should be placed in a folder with the same name as the component class object python script. This folder should be zipped into a file of the same name (jupyter.zip) when it is ready to be installed or distributed.

Example Jupyter Plugin:
```
- jupyter/
  - jupyter.py
```

A plugin is nothing more than a component that is loaded dynamically by Skelebot at runtime. To create a plugin simply create a class that extends the Component object and ensure it is placed in a script that is named the same (albeit with the first letter lower-case). The name of the script should follow camel case (thisIsCamelCase), and the name of the class object should follow pascal case (ThisIsPascalCase).

Example Plugin Script (jupyter.py):
```
from skelebot.objects.component import Compenent, Activation
from skelebot.systems.execution import docker

# This component provides the ability to spin up Jupyter in Docker for any project
class Jupyter(Component):
    activation = Activation.PROJECT
    commands = ["jupyter"]

    port = None
    folder = None

    # Allows for intelligent defaults in the constructor so projects without config can still use the component
    def __init__(self, port=8888, folder="."):
        self.port = port
        self.folder = folder

    # Parser for the command that spins up Jupyter inside the Docker Container based on the given port and folder
    def addParsers(self, subparsers):
        helpMessage = "Spin up Jupyter in a Docker Container (port = {port}, folder = {folder})".format(port=self.port, folder=self.folder)
        parser = subparsers.add_parser("jupyter", help=helpMessage)
        return subparsers

    # Build the docker image and then run the container with the Jupyter command, port mapped, and folder volume mapped
    def execute(self, config, args):

        status = docker.build(config)
        if (status == 0):
            root = " --allow-root" if config.language == "R" else ""
            command = "jupyter notebook --ip=0.0.0.0 --port=8888{root} --notebook-dir={folder}".format(root=root, folder=self.folder)
            ports = ["{port}:8888".format(port=self.port)]

            return docker.run(config, command, "i", ports, ".", "jupyter")
```

#### Activation

The `activation` field of a Component specifies at which point the plugin Component will be available for use. There are four possible options for this field.

- **EMPTY** | Only available when run outside of a Skelebot project (no skelebot.yaml file present)
- **CONFIG** | Only available when the Skelebot project has the specified component attributes present in the config
- **PROJECT** | Available when run inside any Skelebot project
- **ALWAYS** | Always available no matter what

If the field is not specifed, it will default to the `CONFIG` activation level.

#### Attributes

Any attributes you need can be added to the plugin class as long as you specify them in the `__init__` function as well. These attributes will be configurable via the corresponding section of the skelebot.yaml components feild.

The name of the section under components will be the camel case version of the plugin's name.

Example:
```
components:
  jupyter:
    port: 1127
    folder: .
```

### Hooks

There are numerous places that a plugin can hook into the Skelebot systems to augment the tool with new features.

#### Scaffold

```
scaffold(self) # return None
```

The scaffolder provides a scaffold function that can be implemented in the plugin's Component class in order to add its own prompts and data into the Skelebot scaffolding process.

The purpose of the scaffold function for a component is to prompt the user for values and assign them to the corresponding attribute in the Component class. These attributes will be automatically recorded int he skelebot.yaml file that is generated.

#### Argument Parsers

```
addParsers(self,
    subparsers # the 'job' subparser from the Skelebot ArgumentParser
) # return subparsers (updated para object)
```

The argument parser for Skelebot provides a hook called `addParsers` to provide a way for components to supply additional parsing options for the Skelebot CLI. This goes hand-in-hand with the `execute` hook that is shon below.

The `addParsers` function accepts a single parameter, `subparsers`, which is a subparser from the main `argparse.ArgumentParser` object of the Skelebot CLI. Documentation for how to use the parser can be found [here](https://docs.python.org/3/library/argparse.html).

Any parser or argument you add to this parser will be attached to the "job" subparser of the main ArgumentParser. This "job" parser is what will be used by the CLI to determine what gets executed by a given Skelebot command.

This function needs to return the altered subparsers object in order to be properly incorporate the changes into the Skelebot parsing system.

#### Append Dockerignore

```
appendDockerignore(self) # return string (additional .dockerignore contents)
```

The process of generating the `.dockerignore` file for the project can be augmented using the `appendDockerignore` function. This function takes no parameters, and simply appends the string that is returned from the function to the end of the `.dockerignore` file.

#### Append Dockerfile

```
appendDockerfile(self) # return string (additional Dockerfile contents)
```

In the same manner as the `appendDockerignore` function, the process of generating the `Dockerfile` for the project can be augmented using the `appendDockerfile` function. This function takes no parameters, and simply appends the string that is returned from the function to the end of the `Dockerfile`.

#### Execute

```
execute(self,
    config, # The Class object of the skelebot.yaml config file for the project
    args # The parsed args that were passed to the command through the CLI
) # return None
```

The `execute` function provides a way of performing an action when a command is supplied to the SKelebot CLI. The execute function will be invoked when the `job` argument matches one of the values provided in the Component's commands list attribute.

There is essentially no limit to what can be done inside of a Component's `execute` function.

#### Prepend Command

```
prependCommand(self,
    job, # The Class object for the running job configuration located in the skelebot.yaml file
    native # Boolean flag indicating whether this job will be running in Docker or running natively
) # return string (command to prepend to the normal script execution)
```

During a job's execution it is possible you may want to run an additonal command, such as authenticate with a service prior to calling it. This can be done with the `prependCommand` hook function.

The `job` parameter provides the Class object with all of the config details of the job that is being run, while the `native` parameter supplies a boolean value to indicate whether it is going to be run in Docker or natively (on the local host machine).

This function needs to return a string specifying the bash command that should be executed prior to the job's normal script execution.

#### Append Command

```
appendCommand(self,
    job, # The Class object for the running job configuration located in the skelebot.yaml file
    native # Boolean flag indicating whether this job will be running in Docker or running natively
) # return string (command to prepend to the normal script execution)
```

During a job's execution it is possible you may want to run an additonal command, such as copy a file from the container to the host after the job completes. This can be done with the `appendCommand` hook function.

The `job` parameter provides the Class object with all of the config details of the job that is being run, while the `native` parameter supplies a boolean value to indicate whether it is going to be run in Docker or natively (on the local host machine).

This function needs to return a string specifying the bash command that should be executed after the job's normal script execution.

#### Docker Run Parameters

```
addDockerRunParams(self) # return string (additional parameters to include in the docker run process)
```

The Docker run system can be enhanced by adding additional parameters to the run command. The `addDockerRunParams` function takes no parameters and simply returns a string of parameters to be included in the command during execution.

### Functions

There are also several functions that you can call directly that may be very useful to your plugin.

#### Build Dockerfile

```
skelebot.systems.generators.dockerfile.buildDockerfile(
    config # The Class object of the skelebot.yaml config file for the project
)
```

The `buildDockerfile` function will generate the Dockerfile when provided with the config object.

#### Build Dockerignore

```
skelebot.systems.generators.dockerfile.buildDockerignore(
    config # The Class object of the skelebot.yaml config file for the project
)
```

This function will generate the .dockerignore file when provided with the config object.

#### Docker Build

```
skelebot.systems.execution.docker.build(
    config # The Class object of the skelebot.yaml config file for the project
)

```

The `docker.build` function will build the Docker Image from the given config object.

#### Docker Run

```
skelebot.systems.execution.docker.run(
    config, # The Class object of the skelebot.yaml config file for the project
    command, # The command to execute inside of the docker container
    mode, # The mode in which the Docker run should be executed
    ports, # List of port mappings
    mappings, # List of volume mappings
    taskName # The name of the task that will be appended to the container name
)
```

The `docker.run` function will build the Docker Image from the given config object and command.

The `mode` parameter specifies how the job will run: `i` for interactive, `d` for detached, and `t` for TTY.

The `ports` parameter allows for port mappings to be specified manually with the following format: {host-port}:{container-port}

The `mappings` parameter allows for  the same type of mappings as ports, but for volume maps on the container.

The `taskName` allows you to specify the name of the task to append to the conatiner name.

---

<center><< <a href="jupyter.html">Jupyter</a>  |  <a href="base-images.html">Base Images</a> >></center>
