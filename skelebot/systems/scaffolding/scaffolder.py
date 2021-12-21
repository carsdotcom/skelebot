"""Scaffolder System"""

import os
from ...objects.config import Config
from ...components.componentFactory import ComponentFactory
from ...systems.generators import dockerfile, dockerignore, readme, yaml
from ...common import LANGUAGE_DEPENDENCIES, TEMPLATES
from .prompt import promptUser

def scaffold(existing=True):
    """Scaffold a new Dashboard Project"""

    # Prompt for basic project information
    print("Scaffolding Skelebot Project")
    print("--:-" * 5, "-:--" * 5)
    name = promptUser("Enter a PROJECT NAME")
    description = promptUser("Enter a PROJECT DESCRIPTION")
    maintainer = promptUser("Enter a MAINTAINER NAME")
    contact = promptUser("Enter a CONTACT EMAIL")
    language = promptUser("Select a LANGUAGE", options=list(LANGUAGE_DEPENDENCIES.keys()))
    template = promptUser("Select a TEMPLATE", options=list(TEMPLATES[language].keys()))
    template = TEMPLATES[language][template]

    # Iterate over components for additional prompts and add any components that are scaffolded
    components = []
    componentFactory = ComponentFactory()
    for component in componentFactory.buildComponents():
        component = component.scaffold()
        if (component is not None):
            if (isinstance(component, list)):
                components += component
            else:
                components.append(component)

    # Confirm user input - allow them to back out before generating files
    print("--:-" * 5, "-:--" * 5)
    print("Setting up the", name, "Skelebot project in the current directory")
    print("(", os.getcwd(), ")")
    if (not promptUser("Confirm Skelebot Setup", boolean=True)):
        raise Exception("Aborting Scaffolding Process")

    print("--:-" * 5, "-:--" * 5)
    if (not existing):
        # Setting up the folder structure for the project
        print("Rigging up the skele-bones...")
        for directory in template["dirs"]:
            os.makedirs(directory, exist_ok=True)

        # Setting up the file templates for the project
        print("Attaching fiber optic ligaments...")
        dirname = os.path.dirname(__file__)
        for destination, template_file in template["files"].items():
            with open(os.path.join(dirname, template_file), "r") as tmp_file:
                print(os.path.join(dirname, template_file))
                with open(destination, "w") as dst_file:
                    print(destination)
                    dst_file.write(tmp_file.read())

    print("Soldering the micro-computer to the skele-skull...")
    # Build the config object based on the user inputs
    cfg = template["config"]
    cfg["name"] = name
    config = Config.load(cfg)
    config.description = description
    config.maintainer = maintainer
    config.contact = contact
    config.components = components
    config.version = "0.1.0"

    if (not existing):
        # Creating the files for the project
        print("Uploading default {template.key()} system drivers...")
        dockerfile.buildDockerfile(config)
        dockerignore.buildDockerignore(config)
        readme.buildREADME(config)

    # For existing projects, only the skelebot.yaml file is generated
    yaml.saveConfig(config)
    print("Your Skelebot project is ready to go!")
