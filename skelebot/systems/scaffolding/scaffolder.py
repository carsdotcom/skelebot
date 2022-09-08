"""Scaffolder System"""

import os
import json
import requests
import yaml as pyyaml
from ...objects.config import Config
from ...components.componentFactory import ComponentFactory
from ...systems.generators import dockerfile, dockerignore, readme, yaml
from ...common import LANGUAGE_DEPENDENCIES, TEMPLATES, TEMPLATE_PATH, GITHUB_RAW
from .prompt import promptUser

class Scaffolder:

    existing = None
    variables = None

    def __format_variables(self, text):
        for key, value in self.variables.items():
            key_str = f"{{{key}}}"
            if key_str in text:
                text = text.replace(key_str, value)

        return text

    def __format_config(self, config):
        return eval(self.__format_variables(str(config)))

    def __load_github_template(self, owner, repo, branch="main"):
        url = GITHUB_RAW.format(owner=owner, repo=repo, branch=branch, filepath="template.yaml")
        response = requests.get(url, timeout=10)
        yaml_text = self.__format_variables(response.text)
        template = pyyaml.load(yaml_text, Loader=pyyaml.FullLoader)
        for file_dict in template.get("files", []):
            path = file_dict["template"]
            file_url = GITHUB_RAW.format(owner=owner, repo=repo, branch=branch, filepath=path)
            file_dict["template"] = file_url

        return template

    def __load_template(self, path):
        template = None
        with open(f"{path}/template.yaml", "r") as yaml_file:
            yaml_text = self.__format_variables(yaml_file.read())
            template = pyyaml.load(yaml_text, Loader=pyyaml.FullLoader)

        return template

    def __init__(self, existing=True):
        self.existing = existing
        self.variables = {}

    def scaffold(self):
        """Scaffold a new Dashboard Project"""

        # Prompt for basic project information
        print("Scaffolding Skelebot Project")
        print("--:-" * 5, "-:--" * 5)
        name = promptUser("Enter a PROJECT NAME")
        description = promptUser("Enter a PROJECT DESCRIPTION")
        maintainer = promptUser("Enter a MAINTAINER NAME")
        contact = promptUser("Enter a CONTACT EMAIL")
        language = promptUser("Select a LANGUAGE", options=list(LANGUAGE_DEPENDENCIES.keys()))

        # Configure Template Variables
        self.variables["name"] = name
        self.variables["name_simple"] = name.lower().replace(" ", "_").replace("-", "_")
        self.variables["description"] = description
        self.variables["maintainer"] = maintainer
        self.variables["contact"] = contact
        self.variables["language"] = language

        # Load the Template Config
        options = list(TEMPLATES[language].keys())
        options.append("github:{owner}:{repo}:{branch}")
        template = promptUser("Select a TEMPLATE", options=options, reiterate=False)
        if (template.startswith("github:")):
            template_parts = template.split(":")
            owner = template_parts[1]
            repo = template_parts[2]
            branch = template_parts[3] if (len(template_parts) > 3) else "main"
            template = self.__load_github_template(owner, repo, branch=branch)
        else:
            template_name = TEMPLATES[language][template]
            template_path = TEMPLATE_PATH.format(name=template_name)
            template_path = os.path.join(os.path.dirname(__file__), template_path)
            template = self.__load_template(template_path)

        # Prompt user based on the template
        for prompt in template.get("prompts", []):
            self.variables[prompt["var"]] = promptUser(prompt["message"])

        # Iterate over components for additional prompts and add any components that are scaffolded
        components = []
        componentFactory = ComponentFactory()
        for component in componentFactory.buildComponents():
            component = component.scaffold()
            if (component is not None):
                if (isinstance(component, list)):
                    components += component
                else: components.append(component)

        # Confirm user input - allow them to back out before generating files
        print("--:-" * 5, "-:--" * 5)
        print("Setting up the", name, "Skelebot project in the current directory")
        print("(", os.getcwd(), ")")
        if (not promptUser("Confirm Skelebot Setup", boolean=True)):
            raise Exception("Aborting Scaffolding Process")

        print("--:-" * 5, "-:--" * 5)
        if (not self.existing):
            # Setting up the folder structure for the project
            print("Rigging up the skele-bones...")
            for directory in template.get("dirs", []):
                os.makedirs(directory, exist_ok=True)

            # Setting up the file templates for the project
            print("Attaching fiber optic ligaments...")
            for file_dict in template.get("files", []):
                file_path = file_dict["template"]
                file_body = ""
                if (file_path.startswith("http")):
                    response = requests.get(file_path, timeout=10)
                    file_body = response.text
                else:
                    template_file = f"{template_path}/{file_path}"
                    with open(template_file, "r") as tmp_file:
                        file_body = tmp_file.read()

                with open(file_dict["name"], "w") as dst_file:
                    dst_file.write(self.__format_variables(file_body))

        print("Soldering the micro-computer to the skele-skull...")
        # Build the config object based on the user inputs
        cfg = self.__format_config(template["config"])
        cfg["name"] = name
        config = Config.load(cfg)
        config.description = description
        config.maintainer = maintainer
        config.contact = contact
        config.components = components
        config.version = "0.1.0"

        if (not self.existing):
            # Creating the files for the project
            print("Initializing default systems...")
            dockerfile.buildDockerfile(config)
            dockerignore.buildDockerignore(config)
            readme.buildREADME(config)

        # For existing projects, only the skelebot.yaml file is generated
        yaml.saveConfig(config)
        print("Your Skelebot project is ready to go!")
