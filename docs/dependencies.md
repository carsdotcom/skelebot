[Home](index.md)

---

# Dependencies

Skelebot offers the ability to list your Python dependencies directly in the skelebot.yaml file and have these dependencies installed into your Docker image automatically.

```
...
dependencies:
- numpy=1.11.2
- pandas
- ...
```

By default dependencies are installed using pip install.

Versions for packages can be specified by appending `={version}`, `=={version}`, `>={version}`, etc. to the end of the dependency name. Skelebot supports most of the standard python [version specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/#id5).

Skelebot also supports dependencies to be installed from the local file system, GitHub repo, requirements file, or [`pyproject.toml`](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html) file:

```
dependencies:
- req:requirement.txt
- proj:pyproject.toml
- file:libs/myPackage.tgz
- req:requirements.txt
- github:myGitHub/fakeRepo
- proj:pyproject.toml
```

When using a pyproject file, *all* specified required and optional set(s) of dependencies will be installed.

### CodeArtifact Python Packages

Skelebot also supports pulling Python packages that are stored in AWS CodeArtifact. This requires a good deal of information in order to authenticate and pull the correct asset for the package.

```
dependencies:
- ca_file:{domain}:{owner}:{repo}:{pkg}:{version}:{profile}
```
These values are needed in order to preperly obtain the package and include it in the Docker image.
- domain - The domain name of the AWS CodeArtifact repository (ex: my_domain)
- owner - The owner of the AWS CodeArtifact repository (ex: 111122223333)
- repo - The repository in CodeArtifact where the package is located (ex: my_repo)
- pkg - The name of the Python package to be installed (ex: my_package)
- version - The version of the package to be pulled (ex: 1.0.0)
- profile - [OPTIONAL] The AWS profile on your machine that has access to this CodeArtifact repository (ex: dev)

NOTES:

- When installing via `file:` or `github:` the ability to specify a version is not available.
- Python `github` dependencies may optionally specify a protocol like https (more info [here](https://pip.pypa.io/en/stable/reference/pip_install/#git)).

---

<center><< <a href="docker-host.html">Docker Host</a>  |  <a href="image-commands.html">Image Commands</a> >></center>
