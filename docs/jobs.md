[Home](index.md)

---

# Jobs

Jobs are the core of what makes Skelebot useful. They allow you to explicitly define the different execution sequences that your project offers and provide a simple way for others to find and understand not only what the job does, but how to run it.

Jobs are configured manually inside of the skelebot.yaml file.

```
...
jobs:
- name: example
  source: src/jobs/example.sh
  mode: i
  host: ssh://root@me.local
  help: EXAMPLE JOB
  mappings:
  - data/
  - ~/myname.keytab:~/root/keytabs
  - models/:app/model-output/
  args:
  - name: date
    help: the date on which to pull data for the job
  params:
  - name: env
    alt: e
    default: local
    help: the environment from which the job will pull data
    choices:
    - local
    - dev
    - prod
...
```

A job must contain three things in order to work. It must have a name, so you can call it from the command line, a source file to execute, and a help message for users to understand it. Python projects must utilize the `.py` extension while R projects must utilize the `.R` extension, but Bash scripts `.sh` are supported for both Python and R projects. Jobs can contain several additional fields:

 - **name** - The name that is used to execute the job from the command line
 - **source** - Command to be executed(ex: echo 'Hello') or the path to the script (R, Python, or Bash) that will be executed
 - **help** - Text that will be displayed when the -h (--help) parameter is passed
 - **mode** - The mode in which to execute the docker image [i: interactive(default), d: detached]
 - **host** - The host on which the job should be executed (overrides the global "host" field)
 - **mappings** - Volume maps for docker run in one of the two formats supported: [{project-folder}, {local-folder}:{container-folder}]
 - **ignores** - A list of files, folders, or regex patterns to ignore from the Docker build context
 - **args** - List of required arguments for the job that are passed to the underlying script in the order specified
   - **name** - The name of the argument
   - **choices** - A list of avaialable options for the argument
   - **help** - A message displayed in the help output to describe what the argument does
 - **params** - List of parameters for the job. Parameters are optional and provided using their name (ex: --param 123)
   - **name** - The name of the parameter
   - **alt** - Shorthand name for the parameter, generally a single letter (ex: -p 123)
   - **default** - A default value for the parameter if none is provided
   - **choices** - A list of avaialable options for the parameter
   - **accepts** - Allow for the parameter to accept `boolean` for simple flags and `list` for lists of values
   - **help** - A message displayed in the help output to describe what the parameter does

Executing a job is as simple as passing the job name to the Skelebot command.

In the example below the argument `date` is passed as `2018-01-01` and the parameter `env` is passed as `dev`. These are then passed along to the script `src/jobs/example.sh` inside of a Docker container.

If a job is executed in Docker `default` then any output generated will be generated inside the Docker container, and not on the host machine. As a result, in order to get output files from jobs, it is necessary to add the output folder to the `mappings` list in the job's config.

```
> skelebot example 2018-01-01 --env dev
```

### Global Job Parameters
Often times you may have the same parameter that applies to every job in the project, such as setting the log level. For this situation Skelebot offers the ability to specify global parameters that apply to every job.

These parameters are defined exactly the same way that job parameters are defined, but they are specifed at the root level of the config instead of inside the config of a single job. When a parameter is specified in the root level params list, it will be applied to each job that is defined in the config.

```
...
jobs:
- ...
params:
- name: log-level
  alt: l
  default: info
  help: The level at which logs should be output from the jobs
  choices:
  - debug
  - info
  - warn
  - error
  - critical
...
```

### Mapping Ports
Skelebot provides the `ports` property in the skelebot.yaml config file for specifying on which ports jobs will run and expose their services. This property accepts a list of strings of a specific format: `{host-port}:{container-port}`.

The `host-port` specifies the port that is exposed on the host machine. This is the port that you will use to access whatever you may be serving.

The `container-port` specifies the port inside the Docker Container that will be mapped.

Ports can be specified at two different levels.

The global level will apply the port mappings to every job.

```
jobs:
- ...
ports:
- 8080:8080
- 8888:8888
```

The job level will apply the port mappings to only the specified job.

```
jobs:
- name: run
  source: run.py
  help: run the server
  ports:
  - 8080:8888
```

### Primary Job
By default the Docker Image that is built by Skelebot will not run a command, but instead requires skelebot to provide it with a script, arguments, and parameters to run when a job is executed. For the purpose of building images that can be distributed, Skelebot offers a way to specify a job as the project's Primary Job.

```
primaryJob: example
```

This is done by simply using the name of one of the jobs in the `primaryJob` attribute of the config file. This will allow Skelebot to set this job as the default command for the docker image that is built, thereby making a more easily distributable Docker Image for the sake of deployment.

#### Primary Exe
The `primaryExe` field in the skelebot.yaml config allows for the specification of an execution command to use in the Dockerfile. This field accepts two different values: "ENTRYPOINT" and "CMD". If the field is not specified in the config, the default "CMD" value is used.

```
primaryExe: (ENTRYPOINT, CMD)
```

Using "CMD" as the primary execution method requires that the primary job is configured to use only parameters, not arguments, and that each parameter has a default value. This allows the command string to be constructed in full so that it can be run without any extra parameters in the Docker Run command.

In this scenario it is possible to set default parameter values to environment variables to allow for different user's to set different parameter values without altering the manner in which the image is executed.

```
...
jobs:
- name: test
  source: jobs/test.sh
  mode: it
  help: Run the test cases for the project
  params:
  - name: runner
    alt: r
    default: $RUNNER
    help: The name of the person running the tests
```

When using the "ENTRYPOINT" execution method, the parameters and arguments are not used in the construction of the Dockerfile, and instead are left to be inserted during the Docker Run process manually.

Were the example job above to be configured with an "ENTRYPOINT" execution, the params could be specified at runtime in the following manner.

```
docker run my-image --runner ME
```

For more information on the details of "CMD" and "ENTRYPOINT" please refer to [Docker's Documentation](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact).

### Skelebot Parameters
Skelebot has some optional parameters that allow you to control how the jobs are run. These parameters apply to everything in Skelebot, not just the jobs. As such, they are specified in the command line after the skelebot command and before the job argument.

 - **--env (-e)** - Specify the runtime environment configurations (skelebot-{env}.yaml) that will overwrite the default yaml
 - **--skip-build (-s)** - Skip the docker build process and assume the docker image is already constructed and ready to be used
 - **--native (-n)** - Run natively instead of through Docker (NOTE: This will not install any dependencies)
 - **--host (-d) HOST** - Set the Docker Host on which the command will be executed (overrides config level "host" fields)

### Chaining Jobs
Jobs can also be chained together in a single command (executed one after another) by simply concatenating them in the command separated by a `+` character. This allows for multiple jobs to be executed in a single command, and can be a real time saver for long running sequences of jobs.

```
> skelebot query + wrangle --all + train --output-folder results/
```

The example above would first execute the `query` job, followed by the `wrangle` job with the `all` flag set to TRUE, and finally the train job with the `output_folder` set to `results/`.

---

<center><< <a href="image-commands.html">Image Commands</a>  |  <a href="priming.html">Priming</a> >></center>
