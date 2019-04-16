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

Versions for packages, both in R and Python, can be specified by appending '={version}' to the end of the dependency name.

R also supports dependencies to be installed from the local file system as well as from GitHub using the following structure.

```
dependencies:
- {type}:{source}:{name}
- file:libs/myPackage.tgz:mypack
- github:myGitHub/fakeRepo:fakeRepo
```

NOTE: When installing via 'file:' or 'github:' the ability to specify a version is not available.

---

<center><< [Scaffolding](scaffolding.md)  |  [Jobs](jobs.md) >></center>
