[Home](index.md)

---

# Environments

Skelebot supports projects that require multiple configurations for different environments. The skelebot.yaml file will serve as the default configuration for your project. In order to modify the configuration for another environment simply create a new file named `skelebot-{env}.yaml`. This file follows the exact same structure as the normal skelebot.yaml file but only needs to contain values that will override the default values.

To enable an environment, pass the `-e (--env)` parameter followed by the name of the environment when executing a command.

```
> skelebot -e local -h
```

Environment configurations can override any property in the skelebot yaml, even jobs, but keep in mind that any attribute in the environemtn config will completely override the attribute from the default config. This means if you want to change a child attribute, everything under that parent will need to be included in the config as well.

---

<center><< <a href="docker-ignores.html">Docker Ignores</a>  |  <a href="versioning.html">Versioning</a> >></center>
