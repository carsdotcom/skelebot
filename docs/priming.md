[Home](index.md)

---

# Priming

Skelebot generates files, such as the Dockerfile, based on the contents of the skelebot.yaml file. These files are generated (or regenerated) whenever a job is executed, but they can also be generated manually if needed. The `prime` command in Skelebot will generate the needed files and build the Docker Image to prime Skelebot for execution, or to prepare for deployment.

```
> skelebot prime
```

Once complete the .dockerignore file and the Dockerfile will be visible in your project folder, unless you have your project set to `ephemeral` mode. The Docker Image for the project will also be built with the primary job set as the run command, as specified in the skelebot.yaml.

```
> skelebot prime --output my-image.img
```

Skelebot can also save the Docker image as a file if you provide the file location to the command with the "output" parameter.

---

<center><< <a href="jobs.html">Jobs</a>  |  <a href="docker-ignores.html">Docker Ignores</a> >></center>
