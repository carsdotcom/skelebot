[Home](index.md)

---

# Docker Ignores

When a docker build is run, any file contained within the root folder of the project (or any sub-folders) will be added to the Docker context. This process can be slow and can also end up using a lot of memory, especially with large files such as data files. For that reason, Skelebot generates a file called '.dockerignore' from the ignore list in the skelebot.yaml file. Anything included in the ingore list will not be added to the context.

```
...
ignores:
- .RData
- .pkl
- .csv
- .model
...
```

---

<center><< <a href="priming.html">Priming</a>  |  <a href="environments.html">Environments</a> >></center>
