[Home](index.md)

---

# Scaffolding Template

Scaffolding Templates can be setup inside of Git repositories in order to allow for custom scaffolding from within the Skelebot Scaffold command.

At a minimum, a template.yaml file is required at the root directory of the repository.

```
prompts:
  - var: package_name
    message: "Enter A Python Package Name"

dirs:
- "jobs/"
- "{package_name}/"

files:
- name: "Jenkinsfile"
  template: files/Jenkinsfile
- name: "{package_name}/__init__.py"
  template: files/blank
- name: "{package_name}/scorer.py"
  template: files/scorer.py
- name: "{package_name}/trainer.py"
  template: files/trainer.py
- name: "jobs/scorer.py"
  template: files/scorer.py
- name: "{package_name}/trainer.py"
  template: files/trainer.py

config:
    dependencies:
    - pandas~=1.1
    - numpy~=1.19
    commands:
    - "pip install ."
    primaryJob: score
    jobs:
    - name: train
      source: jobs/train.py
      help: "Train the Model"
    - name: retrain
      source: jobs/retrain.py
      help: "Re-Train the Model"
    - name: score
      source: jobs/score.py
      mappings:
      - "~/.aws/:/root/.aws/"
      help: "Perform Batch-Mode Scoring in Docker"
```

### Prompting for Details
If you need to extra details that are not included in the default Skelebot scaffolding prompts, new prompts can be added for your specific template.

Prompts can be specified with the `prompts` list attribute in the template yaml file using a `var`, or variable name, and a `message` that will be shown to the user. You can use this to specify any number of prompt-based variables that you need.

```
prompts:
  - var: package_name
    message: "Enter A Python Package Name"
```

### Using Variables
The default scaffolding process will prompt for and store a number of variables prior to the template being loaded.

#### Default Variables
- **name** - The PROJECT NAME
- **simple_name** - A lowercase version of the PROJECT NAME with spaces and dashes converted to underscores
- **description** - The PROJECT DESCRIPTION
- **maintainer** - The MAINTAINER NAME
- **contact** - The CONTACT EMAIL

These variables, as well as any variables setup by the template's `prompts`, can be used within the template.yaml and any file templates as well by using the `{variable_name}` syntax.

```
config:
    name: {name}
```

### Scaffolding Directories
The `dirs` list attribute can be used to specify any directories that need to be created by the scaffolding process.

```
dirs:
- "jobs/"
- "{package_name}/"
```

### Scaffolding Files
The `files` list attribute can be used to specify any files (`name` attribute) that need to be created by the scaffolding process, as well as the template (`template` attribute) that should be used to populate the contents of the files.

```
files:
- name: "Jenkinsfile"
  template: files/Jenkinsfile
- name: "{package_name}/__init__.py"
  template: files/blank
- name: "{package_name}/scorer.py"
  template: files/scorer.py
- name: "{package_name}/trainer.py"
  template: files/trainer.py
- name: "jobs/scorer.py"
  template: files/scorer.py
- name: "{package_name}/trainer.py"
  template: files/trainer.py
```

The template files can be placed anywhere in the repository as long as the path from the root of the repository to the file matches what is configured in the `template` attribute.

### Customizing Skelebot Config
The skelebot.yaml config file can also be scaffolded with the template as well. The `config` attribute accepts all of the same attributes as the normal skelebot.yaml file. (It also accepts variables!)

```
config:
    dependencies:
    - pandas~=1.1
    - numpy~=1.19
    commands:
    - "pip install ."
    primaryJob: score
    jobs:
    - name: train
      source: jobs/train.py
      help: "Train the Model"
    - name: retrain
      source: jobs/retrain.py
      help: "Re-Train the Model"
    - name: score
      source: jobs/score.py
      mappings:
      - "~/.aws/:/root/.aws/"
      help: "Perform Batch-Mode Scoring in Docker"
```

### Usage
To use the template in the scaffolding process you need only to specify the Git clone URL during the scaffolding process. As long as the user has access to the repository, and `git` installed and available in the `$PATH`, it can be cloned and used in the scaffolding process.

<center><< <a href="scaffolding.html">Scaffolding</a>  |  <a href="docker-host.html">Docker Host</a> >></center>
