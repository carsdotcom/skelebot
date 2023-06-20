[Home](index.md)

---

# Artifactory - DEPRECATED v1.11

**The Artifactory component has been deprecated as of v1.11 and should no longer be used. The same functionality (and more) is provided with the Repository component as detailed below. The manner in which the components operate is identical (push and pull commands), they merely utilize a different config structure that allows the Repository component to handle more than just Artifactory repositories.**

---

~~Skelebot currently only supports deploying artifacts to Artifactory. This can be setup by editing the skelebot.yaml file and adding the following `artifactory` section to the components section of the config.~~

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

~~The artifacts field accepts a list of artifacts names and path to the actual artifact object file. The url, repo, and path fields specify where the artifact will end up when it is pushed (or from where it will be pulled).~~

---

# Repository

Skelebot supports the management of artifacts in either Artifactory or S3 with the Repository component. This can be setup by editing the skelebot.yaml file and adding the following `repository` section to the components section of the config.

The example below shows a config with both `s3` and `artifactory` setup as an example, but in practice only one can actually be used in a single config.

```
components:
  repository:
    s3:
      bucket: my-bucket
      region: us-east-1
      profile: dev
    artifactory:
      url: artifactory.me.com
      repo: ml-models
      path: my-model
    artifacts:
      name: model
      file: xgb-model.pkl
      singular: False
```

In order for the S3 setup to work you must have the appropriate credentials and config files setup in your `.aws/` folder. More information on aws credentials can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

The `artifacts` field accepts a list of artifacts names and path to the actual artifact object file. The `url`, `repo`, and `path` fields specify where the artifact will end up when it is pushed (or from where it will be pulled).

The artifacts are defined with three fields.
 - The `name` field is used for renaming the artifact when storing it.
 - The `file` field specifies the location of the file in the project folder structure.
 - The `singular` field is optional and defaults to False. If set to True the artifact will not be appended with a version number when it is pushed. This means there will be only one artifact stored and overrided each time.

### Authentication

A username and password are required for pushing and pulling artifacts to and from Artifactory, but for S3 the credentials are pulled from the `.aws/` folder as mentioned above. The user and password can either be provided via the prompts that display when executing the commands, or they can be passed as parameters in the command itself.

 - `--user (-u)` - The Artifactory username
 - `--token (-t)` - The password associated to the Artifactory username

Skelebot also supports token and api key-based authentication methods for Artifactory either at runtime (using the same above `--token` prompt) or retrieved from AWS Secrets Manager. This can be configured using the optional `auth` subsection:

```
components:
  repository:
    artifactory:
      url: artifactory.me.com
      repo: ml-models
      path: my-model
      auth:
        authType: token         # One of token, api_key, user_pass (default)
        aws: true               # Optionally read auth from secretsManager. Defaults to false
        awsSecret: my-secret    # Defaults to 'Artifactory'
        awsProfile: dev         # Defaults to 'default'
        awsRegion: us-east-1    # Defaults to 'us-east-1'
```

The above configuration will try to retrieve the field `token` from the AWS secret with ID `my-secret` available to users with profile `dev` in region `us-east-1`.

Also note that if `aws: true` then neither username (`-u`) nor password/token/apikey (`-t`) will be asked for at runtime.

### Pushing

To push an artifact that is specified in your skelebot.yaml, simply use the push command along with the name of the artifact.

```
> skelebot push artifact-name
```

When pushing the artifact to the repository, Skelebot will utilize the version number from the config in order to version the artifact. If you attempt to push the same artifact with the same version more than once, you will be prompted with an error message. If you intend on overwriting the artifact, The `-f --force` parameter can be used to forcibly push an existing artifact.

You can also prefix a string of text in front of the artifact name when pushing the artifact to the destination by supplying a string with the `-p --prefix PREFIX` paramater.

### Pulling

To pull an artifact that is specified in your skelebot.yaml file, you can use the pull command with the artifact name and the version you wish to pull.

```
> skelebot pull artifact-name 0.1.0
```

#### Latest Compatible Version

Skelebot allows for the pulling of artifacts based on the project's current version in order to obtain the "latest compatible version". The latest compatible version is the highest version number of the same major version that is not above the project's current version.

Pulling the latest compatible version can be accomplished by specifying "LATEST" as the version number when executing the pull command.

```
> skelebot pull artifact-name LATEST
```

#### ALL Artifacts

For the puposes of automation, or general laziness, Skelebot offers a way to push and pull all of your artifacts in a single command. The keyword `ALL` can be used in place of the artifact name to iterate over each artifact during the push or pull process.

```
> skelebot push ALL
```

When used in conjunction with the `LATEST` keyword this can create a powerful pull command that obtains all of the compatible artifacts for the current version of your project.

```
> skelebot pull ALL LATEST
```

#### Override Artifact

By default the pull command will place the artifact (with the version number) in the root directory of the project. However, you can tell Skelebot to place the artifact in the location that is provided in the config.
This is done with the override parameter (`-o --override`) and would replace the existing artifact in that location automatically, so caution is advised when using this parameter.

```
> skelebot pull artifact-name 1.0.0 --override
```

---

<center><< <a href="publishing.html">Publishing</a>  |  <a href="hdfs-kerberos.html">HDFS Kerberos</a> >></center>
