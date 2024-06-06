[Home](index.md)

---

# Installing

Skelebot requires Python version 3.9 or later to run.

### Pip Install

Skelebot can be installed via pip.

```
> pip install skelebot
```

### Install From Source

To install from source, copy or clone the repository onto your machine. Then, navigate
to the root of the project and execute this command:


```
> pip install .
```

If you do not have proper access on the machine you are using, Skelebot can be installed locally with the following command:

```
> pip install --user .
```

### Development Install

Skelebot developers should first install the package with the additional `dev` dependencies and then test their installation:

```
> pip install .[dev]
> pytest .
```

# Executing

Once it is installed, you will be able to use Skelebot from anywhere on the system with the `skelebot` command.

```
> skelebot
```

---

<center><< <a href="index.html">Home</a>  |  <a href="help-info.html">Help Info</a> >></center>
