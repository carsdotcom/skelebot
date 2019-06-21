[Home](index.md)

---

# Base Images

By default Skelebot will select and use a base image based on the language you have selected for the project (Python or R).

### Without Language

If no language is specified, the image will default to ubuntu:18.04 and some features may not work. Dependencies will also not work when a language is not specified.

### Custom Base Image

```
baseImage: ubuntu:16.04
```

A custom base image can be specified by adding the `baseImage` config field to the top level of the skelebot.yaml. This custom image can be anything, but will need to have the right language based dependencies installed in order to function properly. The custom base image provides flexibility, but the behavior of Skelebot cannot be garunteed when using a custom base image.

---

<center><< <a href="plugins.html">Plugins</a>  |  <a href="index.html">Home</a> >></center>
