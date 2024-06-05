[Home](index.md)

---

# Docker Ignores

When a docker build is run, any file contained within the root folder of the project (or any sub-folders) will be added to the Docker context. This process can be slow, RAM intensive, and result in large docker images. This is especially the with large files, such as data files that are often found in machine learning projects. For this reason, Skelebot generates a file called `.dockerignore` from the ignore list in the skelebot.yaml file. Anything included in the ingore list will not be added to the context.

```
...
ignores:
- '**/*.pyc'
- '**/*.pkl'
- '**/*.csv'
- '**/*.model'
...
```

---

<center><< <a href="priming.html">Priming</a>  |  <a href="environments.html">Environments</a> >></center>
