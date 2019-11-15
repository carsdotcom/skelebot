[Home](index.md)

---

# Artifacts

Skelebot currently only supports deploying artifacts to Artifactory. This can be setup during the scaffolding process or can be manually created by editing the skelebot.yaml file and adding the following `artifactory` section to the components section of the config.

```
components:
  artifactory:
    url: http://my-host:5000/artifactory
    repo: my-repo
    path: path/to/artifact/folder
    artifacts:
      name: artifact-name
      file: path/to/artifact.ext
```

The `artifacts` field accepts a list of artifacts names and path to the actual artifact object file. The `url`, `repo`, and `path` fields specify where the artifact will end up when it is pushed (or from where it will be pulled).

### Pushing

To push an artifact that is specified in your skelebot.yaml, simply use the push command along with the name of the artifact.

```
> skelebot push artifact-name
```

When pushing the artifact to Artifactory, Skelebot will utilize the version number from the config in order to version the artifact. If you attempt to push the same artifact with the same version more than once, you will be prompted with an error message. If you intend on overwriting the artifact, The `-f` parameter can be used to forcibly push an existing artifact.

### Pulling

To pull an artifact that is specified in your skelebot.yaml file, you can use the pull command with the artifact name and the version you wish to pull.

```
> skelebot pull artifact-name 0.1.0
```

A username and token are required for pushing and pulling artifacts to and from Artifactory. These can either be provided via the prompts that
display when executing the commands, or they can be passed as parameters in the command itself.

 - `--user (-u)` - The Artifactory username
 - `--token (-t)` - The token associated to the Artifactory username

#### Latest Compatible Version

Skelebot allows for the pulling of artifacts based on the project's current version in order to obtain the "latest compatible version". The latest compatible version is the highest version number of the same major version that is not above the project's current version.

This can be accomplished by specifying "LATEST" as the version number when executing the pull command.

```
> skelebot pull artifact-name LATEST
```

#### Override Artifact

By default the pull command will place the artifact (with the version number) in the root directory of the project. However, you can tell Skelebot to place the artifact in the location that is provided in the config.
This is done with the override parameter (`-o --override`) and would replace the existing artifact in that location automatically, so caution is advised when using this parameter.


```
> skelebot pull artifact-name 1.0.0 --override
```

---

<center><< <a href="publishing.html">Publishing</a>  |  <a href="hdfs-kerberos.html">HDFS Kerberos</a> >></center>
