from .config.config import Config, Job, Param, Kerberos, Artifact, Deploy, Plugin
from .plugin.plugin import pluginScaffold
from .docker.dockerignore import buildDockerignore
from .input.prompt import promptUser
from .globals import VERSION
import sys
import os
import stat

def scaffold(cwd, existing=False):
    languageDeps = {
        "Python":["numpy", "pandas", "scipy", "scikit-learn"],
        "R":["data.table", "here", "stringr", "readr", "testthat", "yaml"]
    }
    languages = list(languageDeps.keys())

    skelebotHome = os.path.expanduser("~/.skelebot")
    if (os.path.exists(skelebotHome) == False):
        os.makedirs(skelebotHome, exist_ok=True)
        os.makedirs(skelebotHome + "/plugins", exist_ok=True)

    # Prompt for basic project information
    print("-:--" * 10, "SKELEBOT", "--:-" * 10)
    name = promptUser("Enter a PROJECT NAME")
    description = promptUser("Enter a PROJECT DESCRIPTION")
    maintainer = promptUser("Enter a MAINTAINER NAME")
    contact = promptUser("Enter a CONTACT EMAIL")
    language = promptUser("Enter a LANGUAGE", options=languages)

    # Prompt for plugin activations
    availablePlugins = os.listdir(skelebotHome + "/plugins")
    plugins = []
    activate = True
    while activate == True and len(availablePlugins) > 0:
        activate = promt("Would you like to activate a plugin", boolean=True)
        if (activate):
            pluginName = promptUser("Enter the PLUGIN NAME", options=availablePlugins)
            availablePlugins.remove(pluginName)
            pluginConfig = pluginScaffold(pluginName)
            plugin = Plugin(pluginName, pluginConfig)
            plugins.append(plugin)

    # Prompt for artifact information
    artifacts = None
    if (promptUser("Would you like to add an ARTIFACTORY DEPLOYMENT", boolean=True)):
        artName = promptUser("Enter the ARTIFACT NAME")
        artFile = promptUser("Enter the ARTIFACT FILE")
        artUrl = promptUser("Enter the ARTIFACTORY URL")
        artRepo = promptUser("Enter the ARTIFACTORY REPO")
        artPath = promptUser("Enter the ARTIFACTORY PATH")
        artifacts = []
        deployArtifactory = Deploy("Artifactory", artUrl, artRepo, artPath)
        artifact = Artifact(artName, artFile, deployArtifactory)
        artifacts.append(artifact)

    # Prompt for kerberos information
    kerberos = None
    if (promptUser("Enable Kerberos for Hadoop", boolean=True)):
        hdfsUser = promptUser("Enter HDFS USERNAME")
        keytab = promptUser("Enter KEYTAB FILE LOCATION")
        krbConf = promptUser("Enter KERBEROS CONFIG FILE LOCATION")
        kerberos = Kerberos(hdfsUser, keytab, krbConf)

    # Build config objects
    exampleJob = "src/jobs/example.sh"
    args = [Param("date", None, None, None)]
    params = [Param("env", "e", "local", ["local", "dev", "prod"])]
    defaultJobs = [Job("example", exampleJob, "EXAMPLE JOB", args, params)]
    ignore = [".RData", ".pkl", ".csv", ".model"]
    config = Config(name, description, "0.1.0", VERSION, maintainer, contact, language,
                    kerberos, None, languageDeps[language], ignore, defaultJobs,
                    artifacts, None, False, plugins)

    # Confirm user input
    print("-:--" * 10, "SKELEBOT", "--:-" * 10)
    print("Setting up the", name, "Skelebot project in the current directory")
    print("(", cwd, ")")
    if (promptUser("Confirm Skelebot Setup", boolean=True) == False):
        sys.exit(0)

    # Start building the skelebot
    print("-:--" * 10, "SKELEBOT", "--:-" * 10)

    if (existing == False):
        # Setting up the folder structure for the project
        print("Wiring up the skele-bones...")
        os.makedirs("config/", exist_ok=True)
        os.makedirs("data/", exist_ok=True)
        os.makedirs("models/", exist_ok=True)
        os.makedirs("notebooks/", exist_ok=True)
        os.makedirs("output/", exist_ok=True)
        os.makedirs("queries/", exist_ok=True)
        os.makedirs("src/jobs/", exist_ok=True)
        os.makedirs("src/wrangling/", exist_ok=True)
        os.makedirs("src/training/", exist_ok=True)
        os.makedirs("src/scoring/", exist_ok=True)
        os.makedirs("src/testing/", exist_ok=True)

        # Creating the files for the project
        print("Soldering the micro-computer to the skele-skull...")
        config.generateREADME()
        config.generateGitignore()
        config.generateFile(buildDockerignore(config), ".dockerignore")
        config.generateFile("# Local Environment Config", "config/local.yaml")
        config.generateFile("# Development Environment Config", "config/dev.yaml")
        config.generateFile("# Staging Environment Config", "config/stage.yaml")
        config.generateFile("# Disaster Recovery Environment Config", "config/dr.yaml")
        config.generateFile("# Production Environment Config", "config/prod.yaml")
        config.generateFile("", ".here")
        config.generateFile("echo \"This script is just a placeholder example skelebot job. [$1 $2 $3]\"", exampleJob)
        st = os.stat(exampleJob)
        os.chmod(exampleJob, st.st_mode | stat.S_IEXEC)

    config.generateYaml()
    print("Your Skelebot project is ready to go!")
