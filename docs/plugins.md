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
A Skelebot plugin is nothing more than a folder with two python files in it that was been zipped into a single file. Expanded, it would look something like this:

```
 testPlugin
 ├── command.py
 └── scaffold.py
 ```

 The name of the parent folder (more accurately: the name of the zip file) will become the name of the plugin.

 The two files within the folder must be named command.py and scaffold.py in order for Skelebot to understand them.

### Scaffolding
Each Skelebot plugin can optionally extend the scaffolding command to add their own user prompts for config that will be persisted to the skelebot.yaml file. In order to persist the values obtained from the scaffolding extension, the function inside the scaffold.py script must return a dictionary of the configuration details.

Below is a simple example where the user is prompted for a GitHub url which is then returned from the function inside a dictionary.

```
def scaffold():
   url = input("Please enter the project's GitHub URL: ")
   return {"github": url}
```

Once installed the scaffolding process would allow the user to activate this plugin by name, which would then kick off this scaffold function and prompt for a GitHub url. This data is then placed into the skelebot.yaml file during the scaffolding process so that it can be used during the execution of the plugin's command.

### Command
Each Skelebot plugin needs to specify a command. This is the bare minimum for a Skelebot plugin.

In order to specify a command for the plugin you must create a command.py file in the plugin folder with a single function defined within. The function must be named `command` and accept only two parameters `config` and `pluginConfig`. The first parameter, config, is the object that holds the config from the entire skelebot.yaml file. The second parameter, pluginConfig, holds only the config for the current plugin in order to make it more convenient to access the information that is relevant to the plugin itself.

Below is a simple example where the command simply prints the name of the project GitHub url that was prompted and provided through the scaffolding process as a result of the scaffold.py script above. The command returns `True` to indicate that the it executed successfully.

```
def command(config, pluginConfig):
    print(pluginConfig["github"])
    return True
```

This command would then be executed using the plugin name.

```
> skelebot testPlugin
http://www.github.com/mystuff/myrepo
```

---

<center><< [Jupyter](jupyter.md)  |  [Home](index.md) >></center>
