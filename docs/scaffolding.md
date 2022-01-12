[Home](index.md)

---

# Scaffolding

Scaffolding is a mechanism in Skelebot that allows for new projects to be created as Skelebot projects, as well as existing projects to be converted to Skelebot projects.

This task is only available when inside a folder that does not already contain a skelebot.yaml file (i.e. not already a Skelebot project). Inside a folder that contains the skelebot.yaml, this task will not be presented and executing the command will result in an error.

### New Projects
To scaffold a new project, navigate to an empty folder, execute `skelebot scaffold`, and follow the prompts.

```
> skelebot scaffold
```

### Existing Projects
To add Skelebot support to an existing project you can run the scaffolding command with the `existing` param `(--existing, -e)`. This will walk you through the same prompts but will only create the necessary skelebot files instead of the full project structure.

```
> skelebot scaffold -e
```

### Prompts
The scaffolding command will prompt for information required in order to generate the project yaml and structure. Once you have answered all the prompts and the scaffolding is complete you will have a Skelebot project that is ready to be used.

### Templates
The scaffolder will prompt you to select a template based on the language you selected. Currently the only option that is available is a Dash template for quickly getting a dashboard up and running in Python.

```
>> CARS.COM | skelebot scaffold
-:---:---:---:---:---:---:---:---:---:-- SKELEBOT --:---:---:---:---:---:---:---:---:---:-
Enter a PROJECT NAME (no spaces): my-ml-project
Enter a PROJECT DESCRIPTION: A Machine Learning Project
Enter a MAINTAINER NAME: Firstname Lastname
Enter a CONTACT EMAIL: flastname@gmail.com
Select a LANGUAGE [Python, R]: Python
Select a TEMPLATE [Default, Dash]: Dash
-:---:---:---:---:---:---:---:---:---:-- SKELEBOT --:---:---:---:---:---:---:---:---:---:-
Setting up the my-ml-project Skelebot project in the current directory
( /Users/seanshookman/Code/git.cars.com/cml/skelebot/temp )
Confirm Skelebot Setup (Y/n): y
-:---:---:---:---:---:---:---:---:---:-- SKELEBOT --:---:---:---:---:---:---:---:---:---:-
Wiring up the skele-bones...
Soldering the micro-computer to the skele-skull...
Your skelebot is ready to go!
```

### Results
Scaffolding will always create the skelebot.yaml file, which is what defines the projects as a Skelebot project.

If scaffolding is run without the `--existing` flag, it will also create several folders for storing data, models, notebooks,  queries, output, and code.

The structure produced is merely a suggestion and does not need to be adhered to in order for Skelebot to function properly. The only thing Skelebot actually needs is the skelebot.yaml file and the VERSION file. Once you have these files in your project, you can execute the help command, `skelebot --help` and get started using it right away.

---

<center><< <a href="help-info.html">Help Info</a>  |  <a href="dependencies.html">Dependencies</a> >></center>
