[Home](index.md)

---

<h1 align='center'>Skelebot API</h1>
<div align='center'>Version 2</div>

---

### Purpose

Skelebot exposes a number of functions that can be called inside of a plugin in order to execute
and leverage important parts of the Skelebot System.

This document specifies the API contract for v2 of Skelebot.

There are packages and classes outside of this API that are technically accessible via Skelebot,
but since they are not included in this specification, they are not part of the v2 contract for
Skelebot. As such it is not advised to use any function or Class that is not specified in this
document because it may be subject to change throughout iterations of v2.

---

### APIs

- [Common](api/common.md)
- Objects
  - [Component](api/component.md) -- The base object for Plugins to allow them to hook into the Skelebot Systems
  - [SkeleYaml](api/skeleyaml.md) -- The base object for any config Class that needs to be marshalled to/from YAML
- Execution
  - [Docker](api/docker.md) -- The Docker execution functions for building images and running containers
- Generators
  - [YAML](api/yaml.md) -- The YAML generator for saving and loading config from skelebot.yaml
  - [Dockerfile](api/dockerfile.md) -- The Dockerfile generator for constructing the project Dockerfile
  - [Dockerignore](api/dockerignore.md) -- The dockerignore generator for constructing the project .dockerignore
- Scaffolding
  - [Prompt](api/prompt.md) -- The function used to present prompts to the user for scaffolding purposes

---

<center><< <a href="timezone.html">Timezone</a>  |  <a href="index.html">Home</a> >></center>
