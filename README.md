<!--
<div align="center">
  <img src="https://www.cars.com/react-shop-webapp/static/cars-logo.c3ccfb95f1c14e7c071e1d3d8c44d28c.png"><br><br>
</div>
-->
![Version](https://img.shields.io/badge/dynamic/xml.svg?style=plastic&color=green&label=version&query=.&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcarsdotcom%2Fskelebot%2Fmaster%2FVERSION)
[![CircleCI token](https://img.shields.io/circleci/token/cb75132d9ffe340a42dd5deea2f0fff43eb61042/project/github/carsdotcom/skelebot/master.svg?style=plastic)](https://circleci.com/gh/carsdotcom/skelebot)
[![codecov](https://codecov.io/gh/carsdotcom/skelebot/branch/master/graph/badge.svg)](https://codecov.io/gh/carsdotcom/skelebot)

# Skelebot <!--TODO: Replace this with LOGO/MASCOT -->

**Machine Learning Project Management Tool**

---

## About

Skelebot is a command-line tool for managing machine learning projects and executing them in Docker. The purpose of Skelebot is to simply make the life of a Data Scientist easier by doing a lot of the legwork for mundane tasks automatically through a unified, consistent interface.

```
[/code/my-iris-model] > skelebot -h
usage: skelebot [-h] [-e ENV] [-s] [-n]
                {loadData,train,score,jupyter,push,pull,plugin,bump,prime,exec}
                ...

Iris Example
Example Skelebot Project
-----------------------------------
Version: 0.2.1
Environment: None
Skelebot Version (project): 0.2.1
Skelebot Version (installed): 0.2.0
-----------------------------------

positional arguments:
  {loadData,train,score,jupyter,push,pull,plugin,bump,prime,exec}
    loadData            Load the Iris Dataset and save it into the data folder for the train job to access (src/loadData.py)
    train               Use the data loaded in the loadData job to train the iris model (src/train.py)
    score               Use the model that was built in the train job to score new data against the iris model (src/score.py)
    jupyter             Spin up Jupyter in a Docker Container (port = 8888, folder = .)
    push                Push an artifact to artifactory
    pull                Pull an artifact from artifactory
    plugin              Install a plugin for skelebot from a local zip file
    bump                Bump the skelebot.yaml project version
    prime               Generate Dockerfile and .dockerignore and build the docker image
    exec                Exec into the running Docker container

optional arguments:
  -h, --help            show this help message and exit
  -e ENV, --env ENV     Specify the runtime environment configurations
  -s, --skip-build      Skip the build process and attempt to use previous docker build
  -n, --native          Run natively instead of through Docker
```

## Install

Install Skelebot with Pip:

```
pip install skelebot
```

## Getting Started

To get started using Skelebot you can follow the documentation found [here](https://carsdotcom.github.io/skelebot/).

## Contributing

Anyone is welcome to make contributions to the project. If you would like to make a contribution, please read our [Contributor Guide](CONTRIBUTING.md).

## Versioning

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Please refer to the [Changelog](CHANGELOG.md) for information regarding the differences between versions of the project.
