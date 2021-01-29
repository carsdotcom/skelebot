[Home](index.md)

---

# Image Commands

You may need to add additional commands to your Docker image at some point for one reason or another.
Skelebot allows for this by providing a section in the `skelebot.yaml` file called `commands`. These
commands will be built into the Dockerfile after the project dependencies have been installed and
after the project files have been copied over to the image.

```
...
commands:
- apt-get install some-tool-or-library
- curl https://www.not-a-real-website-by-any-stretch.get.a.file.com
- ...
```

If something needs to be installed on the image prior to the dependencies being installed it is best
to build a new image with that already installed and simply alter the base image that Skelebot uses.

---

<center><< <a href="dependencies.html">Dependencies</a>  |  <a href="jobs.html">Jobs</a> >></center>
