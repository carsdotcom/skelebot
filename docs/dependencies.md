[Home](index.md)

---

# Dependencies

For both R and Python projects, Skelebot offers the ability to list your dependencies directly in the skelebot.yaml file and have these dependencies installed into your Docker image automatically.

```
...
dependencies:
- data.table=1.11.2
- stringr
- ...
```

By default R dependencies are installed using install.packages from CRAN.

By default Python dependencies are installed using pip install.

Versions for packages in R can be specified by appending `={version}` to the end of the dependency name.

Versions for packages in Python can be specified by appending `={version}` or `=={version}` to the end of the dependency name.

R and Python also both support dependencies to be installed from the local file system as well as from GitHub using the following structure.
Python also allows for installs using a text file via `req:requirements.txt` syntax.

```
language: R
dependencies:
- {type}:{source}:{name}
- file:libs/myPackage.tgz:mypack
- github:myGitHub/fakeRepo:fakeRepo
```

```
language: Python
dependencies:
- {type}:{source}
- file:libs/myPackage.tgz
- req:requirements.txt
- github:myGitHub/fakeRepo
```

### CodeArtifact Python Packages

Skelebot also supports pulling Python packages that are stored in AWS CodeArtifact. This requires a good deal of information in order to authenticate and pull the correct asset for the package.

```
language: Python
dependencies:
- ca_file:{profile}:{domain}:{owner}:{repo}:{pkg}:{version}:{asset}
```
These are the values that needed to be provided (separated by colons) in order to preperly obtain the package and include it in the Docker image.
- profile - The AWS profile on your machine that has access to this CodeArtifact repository (ex: dev)
- domain - The domain name of the AWS CodeArtifact repository (ex: my_domain)
- owner - The owner of the AWS CodeArtifact repository (ex: 111122223333)
- repo - The repository in CodeArtifact where the package is located (ex: my_repo)
- pkg - The name of the Python package to be installed (ex: my_package)
- version - The version of the package to be pulled (ex: 1.0.0)
- asset - The name of the wheel asset that will actually be used for installation (ex: my_package-1.0.0-py3-none-any.whl)

NOTES:

- When installing via `file:` or `github:` the ability to specify a version is not available.
- Python `github` dependencies may optionally specify a protocol like https (more info [here](https://pip.pypa.io/en/stable/reference/pip_install/#git)).

---

<center><< <a href="docker-host.html">Docker Host</a>  |  <a href="image-commands.html">Image Commands</a> >></center>
