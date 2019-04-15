[Home](index.md) > Copy Commands

---

# Copy Commands

If your project or job requires folders or files to be in a certain place in the docker container that does not match the project structure, Skelebot provides copy commands that allow you to copy the files from your project to specific locations on the docker image during the Docker build phase with the 'copy' field in the skelebot.yaml file.

```
...
copy:
- path/to/src:path/to/container/destination
...
```

The copy field accepts a list of strings. Each string represents a single Docker COPY command. The copy string must be a source file/folder location in the project folder, followed by a colon, followed by the destination fiele/folder in the container.

Due to the fact that these COPY commands will be placed in the Dockerfile in the order they are provided, it is advised that you keep the larger folders at the top and folders that are subject to change at the bottom. This will help by allowing Docker to load large copy commands from the cache.
