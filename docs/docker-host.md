[Home](index.md)

---

# Docker Host

Skelebot offers the ability to run your docker commands on another host aside from your local
machine. To specify a different host for the entire project, simply add the `host` field to the
root of your skelebot.yaml config file.

```
host: ssh://root@remote.host
```

The same parmeter is available at the job-level, and will override the global field if specified.
Skelebot also offers an optional parameter for setting the docker host when running a command.
This value would override anything present in the skelebot.yaml config. More information on both of
these can be found [here](jobs.md).

---

<center><< <a href="scaffolding.html">Scaffolding</a>  |  <a href="dependencies.html">Dependencies</a> >></center>
