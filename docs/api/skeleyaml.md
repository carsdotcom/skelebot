[Home](../index.md) > [API](../api.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 2</div>

---

- [Common](common.md)
- Objects
  - [Component](component.md) -- The base object for Plugins to allow them to hook into the Skelebot Systems
  - **SkeleYaml** -- The base object for any config Class that needs to be marshalled to/from YAML
- Execution
  - [Docker](docker.md) -- The Docker execution functions for building images and running containers
- Generators
  - [YAML](yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<h1 align='center'>SkeleYaml Module</h1>

The SkeleYaml module holds the class required for creating objects with the ability to be converted
to and from YAML formatted Dicts for the sake of reading and persisting data to yaml format.

---

<h2 align='center'>SkeleYaml (Class)</h2>

<h3 align='left'>Import</h3>

```
from skelebot.objects.component import Activation
```

The SkeleYaml class is intended to be used as a Parent Class for any object that needs to be
written to the skelebot.yaml file. As such, the Component class is also a child of the SkeleYaml
class. This means that each Component is capable of having it's attributes written into and read
from the skelebot.yaml by default.

The ability to override the toDict method provides more flexibility for Plugin developers to
augment their Components with further customization.

<h3 align='left'>Attributes</h3>

| NAME   | TYPE                                         | DESCRIPTION                                                                                                      |
|--------|----------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| schema | [Schema](https://github.com/keleshev/schema) | The Schema definition for the object's attributes such that the Dict data can be validated prior to being loaded |

<h3 align='left'>load(cls, config)</h3>

> return cls()

| PARAMETER | TYPE | DESCRIPTION                                                                          |
|-----------|------|--------------------------------------------------------------------------------------|
| config    | Dict | The Dictionary representation of the skelebot.yaml data to be loaded into the object |

```
The purpose of the `load` method is to instantiate a new instance of the class object based on the
Dict config data provided to the method. This data is loaded by Skelebot from the skelebot.yaml
from the corresponding component section of the yaml file.

The default logic of this function will allow for a simple object with non-object type attributes
to be loaded automatically. Unless there are objects within your SkeleYaml object, or some special
logic that is needed at load time, this method can be left to it's default implementation.

If this method is overridden, it must return the instantiated class object (`cls()`).
```

<h3 align='left'>loadList(cls, config)</h3>

> return cls()

| PARAMETER | TYPE | DESCRIPTION                                                                                        |
|-----------|------|----------------------------------------------------------------------------------------------------|
| config    | List | A List of Dictionary representations of the skelebot.yaml data to be loaded into a list of objects |

```
The loadList is a convenience method that simply invokes the load method of the class in a loop
for each element in the config provided and returns a list of instantiated class objects.
```

<h3 align='left'>validate(cls, config)</h3>

> return cls()

| PARAMETER | TYPE | DESCRIPTION                                                                              |
|-----------|------|------------------------------------------------------------------------------------------|
| config    | Dict | The Dictionary representation of the skelebot.yaml data to be validated prior to loading |

```
The validate method utilizes the skeleYaml's schema attribute to perform validation on the provided
Dictionary config data prior to the data being loaded into the object.

This is called from the default implementation of the load method, and should always be invoked
prior to loading a SkeleYaml object.
```

<h3 align='left'>toDict(self)</h3>

> return Dict

```
The toDict method will convert the Child object into a Dict based on the names and values of it's
attributes.

The default implementation of this method will handle simple objects without any additional need
for custom logic. If your object requires specific conversion logic in order to match a certain
format for YAML output, this method can be overridden or augmented by retaining a 'super' call back
to the parent method.

This method must return a Dict such that it can be written as a YAML formatted file.
```

---
