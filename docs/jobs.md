[Home](index.md)

---

# Jobs

Jobs are the core of what makes Skelebot useful. They allow you to explicitly define the different execution sequences that your project offers and provide a simple way for others to find and understand not only what the job does, but how to run it.

Jobs are configured manually inside of the skelebot.yaml file. Any project scaffolded without the '--existing' flag will contain the example job shown below by default.

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
  params:
  - name: env
    alt: e
    default: local
    choices:
    - local
    - dev
    - prod
...
```

A job must contain two things in order to work. It must have a name, so you can call it from the command line, and it must have a source file
to execute. Python projects must utilize the '.py' extension while R projects must utilize the '.R' extension, but Bash scripts '.sh' are supported for both Python and R projects. Jobs can contain several additional fields:

 - **name** - The name that is used to execute the job from the command line
 - **source** - The path to the script (R, Python, or Bash) that will be executed
 - **mode** - The mode in which to execute the docker image [i: interactive(default), d: detached]
 - **help** - Text that will be displayed when the -h (--help) parameter is passed
 - **mappings** - Volume maps for docker run in one of the two formats supported: [{project-folder}, {local-folder}:{container-folder}]
 - **ignores** - A list of files, folders, or regex patterns to ignore from the Docker build context
 - **args** - List of arguments for the job that are passed to the underlying script in the order specified
   - **name** - The name of the argument
   - **default** - A default value for the argument if none is provided
   - **choices** - A list of avaialable options for the argument
 - **params** - List of parameters for the job. Parameters are optional and provided using their name (ex: --param 123)
   - **name** - The name of the parameter
   - **alt** - Shorthand name for the parameter, generally a single letter (ex: -p 123)
   - **default** - A default value for the parameter if none is provided
   - **choices** - A list of avaialable options for the parameter
   - **isBoolean** - If this is set to True, the param will be treated as boolean and only requires the name or alt value to be set

Executing a job is as simple as passing the job name to the Skelebot command.

In the example below the argument (date) is passed as '2018-01-01' and the parameter (env) is passed as 'dev'. These are then passed along to the script 'src/jobs/example.sh' inside of a Docker container.

If a job is executed in Docker (default) then any output generated will be generated inside the Docker container, and not on the host machine. As a result, in order to get output files from jobs, it is necessary to add the output folder to the 'mapped' list in the job's config.

```
> skelebot example 2018-01-01 --env dev
```

**Skelebot Parameters**
Skelebot has some optional parameters that allow you to control how the jobs are run.

 - **--env (-e)** - Specify the runtime environment configurations (skelebot-{env}.yaml) that will overwrite the default yaml
 - **--skip-build (-s)** - Skip the docker build process and assume the docker image is already constructed and ready to be used
 - **--native (-n)** - Run natively instead of through Docker (NOTE: This will not install any dependencies)

---

<center><< <a href="dependencies.html">Dependencies</a>  |  <a href="priming.html">Priming</a> >></center>
