[Home](index.md)

---

# Docker Ignores

When a docker build is run, any file contained within the root folder of the project (or any sub-folders) will be added to the Docker context. This process can be slow and can also end up using a lot of memory, especially with large files such as data files. For that reason, Skelebot generates a file called '.dockerignore' from the ignore list in the skelebot.yaml file. Anything included in the ingore list will not be added to the context.

```
...
ignore:
- .RData
- .pkl
- .csv
- .model
...
```

Skelebot also supports ignore lists at the job level. This allows for different jobs to include or exclude different files or folders
from the Docker context, thereby speeding up the build/run process.

```
...
jobs:
- name: test
  source: src/jobs/test.R
  help: Run the test cases
  ...
  ignore:
  - training-data/
  - scoring-data/
...
```

---

<center><< [Priming](priming.md)  |  [Environments](environments.md) >></center>
