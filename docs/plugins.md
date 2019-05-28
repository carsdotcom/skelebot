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

[TODO] Folder Structure

A plugin is nothing more than a component that is loaded dynamically by Skelebot at runtime. To create a plugin simply create a Class that extends the Component object and ensure it is placed ina script that is named the same (albeit with the first letter lower-case).

Example:
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

## Activation

The 'activation' field specifies at which point the plugin Component will be available for use. There are four possible options for this field.

- **EMPTY** | Only available when run outside of a Skelebot project (no skelebot.yaml file present)
- **CONFIG** | Only available when the Skelebot project has the specified component attributes present in the config
- **PROJECT** | Available when run inside any Skelebot project
- **ALWAYS** | Always available no matter what

If the field is not specifed, it will default to the 'CONFIG' activation level.

## Attributes

Any attributes you need can be added to the plugin Class as long as you specify them in the '__init__' function as well. These attributes will be configurable via the corresponding section of the skelebot.yaml components feild.

The name of the section under components will be the Camel Case version of the plugin's name.

Example:
```
components:
  jupyter:
    port: 1127
    folder: .
```

### Hooks

There are numerous places that a plugin can hook into the Skelebot process to augment the tool with new features.

## Scaffolder

The scaffolder provides a scaffold function that can be implemented in the plugin's Component class in order to add it's own prompts and data into the Skelebot scaffolding process.

The purpose of the scaffold function for a component is to prompt the user for values and assign them to the corresponding attribute in the Component class. These attributes will be automatically recorded int he skelebot.yaml file that is generated.

```
@function: scaffold(self)
@return: None
```

## Argument Parsers

```
@function: addParsers(self, subparsers)
@param subparsers: The 'job' subparser from the Skelebot ArgParser where you can add your own subparsers and arguments
@return: subparsers
```

## Generators
appendDockerignore(self)
appendDockerfile(self)

## Exection
execute(self, config, args)
prependCommand(self, job, native)
appendCommand(Self, job, native)
addDockerRunParams(self)

### Functions

There are also several functions that you can call directly that may be very useful to your plugin.

## Generators
Build Dockerfile - skelebot.systems.generators.dockerfile.buildDockerfile(config)
Build Dockeringore - skelebot.systems.generators.dockerfile.buildDockerignore(config)

## Exection
Docker Build - skelebot.systems.execution.docker.build(config)
Docker Run - skelebot.systems.execution.docker.run(config, command, mode, ports, mappings, taskName)

---

<center><< <a href="jupyter.html">Jupyter</a>  |  <a href="index.html">Home</a> >></center>
