Machine learning projects are too often just a loose collection of unorganized scripts. Skelebot aims to bring order to that chaos.

---

### Purpose

Skelebot is a command-line tool for developing machine learning projects and executing them in Docker. The purpose of Skelebot is to simply make the life of a Data Scientist easier by doing a lot of the legwork for mundane tasks automatically through a unified, consistent interface.

By allowing jobs to be executed in Docker, it removes the need for the developer to install specific R and Python packages on their own machine, and even removes the need to have R installed at all. Configured jobs in Skelebot also come with the added benefit of built-in help documentation in order to assist others in understanding what jobs your project has, and what those jobs do.

Skelebot also saves developer time by integrating with HDFS through Kerberos automatically. By building on top of a library of pre-built Docker images tailored specifically for Skelebot’s purposes, the process of building the Docker image for a project is greatly reduced. Skelebot also encourages a specific folder structure through it’s scaffolding process thereby introducing consistency across projects and developers. By providing a uniform interface on which to discover the project's jobs it greatly helps to reduce the barrier to entry for newcomers to the project.

---

### Features

 - Get a new or existing ML project up and running in seconds with Skelebot **scaffolding**
 - **Prime** the project to regenerate dependent files and prepare a deployable Docker Image
 - Let Skelebot handle the semantic **version** incrementing for you
 - Manage all of your project's **dependencies** in a single file
 - Execute any job in Docker through Skelebot **job execution** and provide an interface and documentation to others
 - Manually execute and debug any code using **skelebot exec** to access to your Docker container directly
 - Manage your project's versioned **artifacts** in Artifactory or S3
 - Access data from **HDFS** through Kerberos authentication protocols defined in your configuration
 - Provide easily accessible **help documentation** for each of your Skelebot jobs
 - Spin up **Jupyter Notebooks** inside of Docker with all of your code, packages, and data ready to go
 - Create your own Skelebot **Plugin** and add even more functionality

---

### Getting Started
- [Installing](installing.md)
- [Help Info](help-info.md)
- [Scaffolding](scaffolding.md)
- [Docker Host](docker-host.md)
- [Dependencies](dependencies.md)
- [Jobs](jobs.md)
- [Priming](priming.md)
- [Docker Ignores](docker-ignores.md)
- [Environments](environments.md)
- [Versioning](versioning.md)
- [Publishing](publishing.md)
- [Artifacts](artifacts.md)
- [HDFS Kerberos](hdfs-kerberos.md)
- [Jupyter](jupyter.md)
- [Plugins](plugins.md)
- [Base Images](base-images.md)
- [Timezone](timezone.md)
- [API](api.md)
