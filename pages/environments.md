[Home](index.md) > Environments

---

# Environments

Skelebot supports projects that require multiple configurations for different environments. The skelebot.yaml file will serve as the default (production) configuration for your project. In order to modify the configuration for another environment simply create a new file named skelebot-{env}.yaml. This file follows the exact same structure as the normal skelebot.yaml file but only needs to contain values that will override the default values.

To enable an environment, pass the -e (--env) parameter followed by the name of the environment when executing a command.

```
> skelebot -e local -h
```

Environment configurations can override any property in the skelebot yaml, even jobs.
