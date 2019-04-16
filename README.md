<!--
<div align="center">
  <img src="https://www.cars.com/react-shop-webapp/static/cars-logo.c3ccfb95f1c14e7c071e1d3d8c44d28c.png"><br><br>
</div>
-->
![Version](https://img.shields.io/badge/Version-0.1.0-green.svg?style=plastic)
[![CircleCI token](https://img.shields.io/circleci/token/cb75132d9ffe340a42dd5deea2f0fff43eb61042/project/github/carsdotcom/skelebot/master.svg?style=plastic)](https://circleci.com/gh/carsdotcom/skelebot)

# Skelebot <!--TODO: Replace this with LOGO/MASCOT -->

**Machine Learning Project Management Tool**

---

## About

Skelebot is a command-line tool for managing machine learning projects and executing them in Docker. The purpose of Skelebot is to simply make the life of a Data Scientist easier by doing a lot of the legwork for mundane tasks automatically through a unified, consistent interface.

```
[/code/my-iris-model] > skelebot -h
usage: skelebot [-h] [-e ENV] [-s] [-n]
                {plugin,bump,prime,exec,jupyter,push,pull,loadData,train,score}
                ...

Iris Example
Example Skelebot Project
-----------------------------------
Version: 0.1.0
Environment: None
Skelebot Version (project): 0.1.0
Skelebot Version (installed): 0.1.0
-----------------------------------

positional arguments:
  {plugin,bump,prime,exec,jupyter,push,pull,loadData,train,score}
    plugin              Install a plugin for skelebot from a local zip file
    bump                Increment the version of the project
    prime               Prime skelebot with latest config
    exec                Start the Docker container and access it via bash
    jupyter             Start a Jupyter notebook inside of Docker
    push                Push an artifact to artifactory
    pull                Pull an artifact from artifactory
    loadData            Load the Iris Dataset and save it into the data folder for the train job to access (src/loadData.py)
    train               Use the data loaded in the loadData job to train the iris model (src/train.py)
    score               Use the model that was built in the train job to score new data against the iris model (src/score.py)

optional arguments:
  -h, --help            show this help message and exit
  -e ENV, --env ENV     Specify the runtime environment configurations
  -s, --skip-build      Skip the build process and attempt to use previous docker build
  -n, --native          Run natively instead of through Docker
```

## Getting Started

To get started using Skelebot you can follow the documentation found [here](https://carsdotcom.github.io/skelebot/).

## Contributing

Anyone is welcome to make contributions to the project. If you would like to make a contribution, please read our [Contributor Code of Conduct](CONTRIBUTING.md).
