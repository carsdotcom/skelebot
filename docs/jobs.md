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

### Primary Job
By default the Docker Image that is built by Skelebot will not run a command, but instead requires skelebot to provide it with a script, arguments, and parameters to run when a job is executed. For the purpose of building images that can be distributed, Skelebot offers a way to specify a job as the project's Primary Job.

```
primaryJob: example
```

This is done by simply using the name of one of the jobs in the `primaryJob` attribute of the config file. This will allow Skelebot to set this job as the default command for the docker image that is built, thereby making a more easily distributable Docker Image for the sake of deployment.

### Skelebot Parameters
Skelebot has some optional parameters that allow you to control how the jobs are run. These parameters apply to everything in Skelebot, not just the jobs. As such, they are specified in the command line after the skelebot command and before the job argument.

 - **--env (-e)** - Specify the runtime environment configurations (skelebot-{env}.yaml) that will overwrite the default yaml
 - **--skip-build (-s)** - Skip the docker build process and assume the docker image is already constructed and ready to be used
 - **--native (-n)** - Run natively instead of through Docker (NOTE: This will not install any dependencies)


### Chaining Jobs
Jobs can also be chained together in a single command (executed one after another) by simply concatenating them in the command separated by a `+` character. This allows for multiple jobs to be executed in a single command, and can be a real time saver for long running sequences of jobs.

```
> skelebot query + wrangle --all + train --output-folder results/
```

The example above would first execute the `query` job, followed by the `wrangle` job with the `all` flag set to TRUE, and finally the train job with the `output_folder` set to `results/`.

---

<center><< <a href="dependencies.html">Dependencies</a>  |  <a href="priming.html">Priming</a> >></center>
