[Home](index.md)

---

# Base Images

By default Skelebot will select and use a base image based on python 3.9. This can be customized by adding the `pythonVersion` config field to the top level of the skelebot.yaml:

```
pythonVersion: '3.11'
```

The desired Python version should be specified as a string.

As of Skelebot v2.0.0, the available versions are 3.9, 3.10, 3.11.


### Custom Base Image

```
baseImage: ubuntu:22.04
```

A custom base image can be specified by adding the `baseImage` config field to the top level of the skelebot.yaml. This custom image can be anything, but will need to have the right language based dependencies installed in order to function properly. The custom base image provides flexibility, but the behavior of Skelebot cannot be guaranteed when using a custom base image.

---

<center><< <a href="plugins.html">Plugins</a>  |  <a href="timezone.html">Timezone</a> >></center>
