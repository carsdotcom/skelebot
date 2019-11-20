[Publishing](publishing.md)

---

# Publishing

Skelebot provides the ability to directly publish the project’s Docker image to a chosen repository based on user config in the skelebot.yaml file. This provides a simple, consistent method to publish the image artifact of a Skelebot project to a repository based on the Skelebot environment.

```
components:
  registry:
    host: repository.cars.com
    port: 5000
    user: skelebot
```

By default the host will be Docker Hub and the port will not be used.

The values that are provided will be structured in the name of the docker image as follows:

```
{host}:{port}/{user}/{project-name}
```

When published the current version of the project will be used as a tag as well as 'latest'.

```
skelebot publish
```

If not logged-in to the provided host in the registry, you will be prompted to enter your username and password.

If you would like to make use of any custom tags when publishing the image, the tags parameter
(`-t --tags`) can be used to specify a list of tag values.

```
skelebot publish --tags LOCAL DEV STAGE
```

---

<center><< <a href="versioning.html">Versioning</a>  |  <a href="artifacts.html">Artifacts</a> >></center>
