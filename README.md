
<p align="center"><img src="logo.gif"></p>
<h1 align="center">Machine Learning Project Development Tool</h1>

[![CircleCI token](https://circleci.com/gh/carsdotcom/skelebot/tree/master.svg?style=svg)](https://circleci.com/gh/carsdotcom/skelebot)
[![codecov](https://codecov.io/gh/carsdotcom/skelebot/branch/master/graph/badge.svg)](https://codecov.io/gh/carsdotcom/skelebot)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d7211eb35681489c9f76066d9a137e46)](https://www.codacy.com/app/sshookman/skelebot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=carsdotcom/skelebot&amp;utm_campaign=Badge_Grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
![Version](https://img.shields.io/badge/dynamic/xml.svg?style=svg&color=purple&label=Dev%20Version&query=.&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcarsdotcom%2Fskelebot%2Fmaster%2FVERSION)
![PyPI](https://img.shields.io/pypi/v/skelebot?color=purple&label=PyPi%20Release)
![PyPI - Downloads](https://img.shields.io/pypi/dm/skelebot?color=purple&label=PyPi%20Installs)

<!--CONTRIBUTORS-->
<table>
  <tr>
    <td align="center" width="150px">
      <a href="https://github.com/sshookman">
        <img src="https://avatars0.githubusercontent.com/u/926448?v=4", width="100px"a><br />
        <sub><b>Sean Shookman</b></sub>
      </a>
    </td>    <td align="center" width="150px">
      <a href="https://github.com/jagmoreira">
        <img src="https://avatars2.githubusercontent.com/u/13685125?v=4", width="100px"a><br />
        <sub><b>Joao Moreira</b></sub>
      </a>
    </td>    <td align="center" width="150px">
      <a href="https://github.com/sherry0531">
        <img src="https://avatars0.githubusercontent.com/u/7463903?v=4", width="100px"a><br />
        <sub><b>Sherry Wang</b></sub>
      </a>
    </td>    <td align="center" width="150px">
      <a href="https://github.com/chutchi2">
        <img src="https://avatars0.githubusercontent.com/u/16807739?v=4", width="100px"a><br />
        <sub><b>Cody Hutchins</b></sub>
      </a>
    </td>    <td align="center" width="150px">
      <a href="https://github.com/kislam01">
        <img src="https://avatars0.githubusercontent.com/u/16831765?v=4", width="100px"a><br />
        <sub><b>Kazi Tanzim Islam</b></sub>
      </a>
    </td>    <td align="center" width="150px">
      <a href="https://github.com/sgaist">
        <img src="https://avatars0.githubusercontent.com/u/898010?v=4", width="100px"a><br />
        <sub><b>Samuel Gaist</b></sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="150px">
      <a href="https://github.com/SanthoshBala18">
        <img src="https://avatars3.githubusercontent.com/u/24211143?v=4", width="100px"a><br />
        <sub><b>SanthoshBala18</b></sub>
      </a>
    </td>
  </tr>
</table>
<!--/CONTRIBUTORS-->

## About

Skelebot is a command-line tool for developing machine learning projects and executing them in Docker. The purpose of Skelebot is to simply make the life of a Data Scientist easier by doing a lot of the legwork for mundane tasks automatically through a unified, consistent interface.

```
[/code/my-iris-model] > skelebot -h
usage: skelebot [-h] [-e ENV] [-s] [-n]
                {loadData,train,score,push,pull,jupyter,plugin,bump,prime,exec}
                ...

Iris Example
Example Skelebot Project
-----------------------------------
Version: 1.1.0
Environment: None
Skelebot Version: 1.8.5
-----------------------------------

positional arguments:
  {loadData,train,score,push,pull,jupyter,plugin,bump,prime,exec}
    loadData            Load the Iris Dataset and save it into the data folder for the train job to access (src/loadData.py)
    train               Use the data loaded in the loadData job to train the iris model (src/train.py)
    score               Use the model that was built in the train job to score new data against the iris model (src/score.py)
    push                Push an artifact to artifactory
    pull                Pull an artifact from artifactory
    jupyter             Spin up Jupyter in a Docker Container (port=8888, folder=.)
    plugin              Install a plugin for skelebot from a local zip file
    bump                Bump the skelebot.yaml project version
    prime               Generate Dockerfile and .dockerignore and build the docker image
    exec                Exec into the running Docker container

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Display the version number of Skelebot
  -e ENV, --env ENV     Specify the runtime environment configurations
  -s, --skip-build      Skip the build process and attempt to use previous docker build
  -n, --native          Run natively instead of through Docker
  -c, --contact         Display the contact email of the Skelebot project
```

## Install

Install Skelebot with Pip:

```
pip install skelebot
```

## Getting Started

To get started using Skelebot you can follow the [Documentation](https://carsdotcom.github.io/skelebot/).

## Contributing

Anyone is welcome to make contributions to the project. If you would like to make a contribution, please read our [Contributor Guide](CONTRIBUTING.md).

## Versioning

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Please refer to the [Changelog](CHANGELOG.md) for information regarding the differences between versions of the project.
