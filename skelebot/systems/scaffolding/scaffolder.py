"""Scaffolder System"""

import os
import re
from subprocess import call

import yaml as pyyaml

from ...objects.config import Config
from ...components.componentFactory import ComponentFactory
from ...systems.generators import dockerfile, dockerignore, readme, yaml
from ...common import TEMPLATES, TEMPLATE_PATH
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

    def __load_git_template(self, url):
        # Construct template_name (folder name) and template path
        template_name = re.sub("[:/\\.@-]+", "_", url)
        template_path = TEMPLATE_PATH.format(name=template_name)
        template_path = os.path.join(os.path.dirname(__file__), template_path)

        # Clone or pull the template from the Git URL into the template folder
        if (os.path.exists(template_path)):
            # If the template has been cloned before, just pull --rebase
            status = call(f"cd {template_path} && git pull --rebase", shell=True)
        else:
            # If the template has NOT been cloned before, clone it
            status = call(f"git clone {url} {template_path}", shell=True)

        return self.__load_template(template_name)

    def __load_template(self, name):
        template = None

        path = TEMPLATE_PATH.format(name=name)
        path = os.path.join(os.path.dirname(__file__), path)
        with open(f"{path}/template.yaml", "r", encoding="utf-8") as yaml_file:
            yaml_text = self.__format_variables(yaml_file.read())
            template = pyyaml.load(yaml_text, Loader=pyyaml.FullLoader)

        # Update file paths in the template
        for file_dict in template.get("files", []):
            file_path = file_dict["template"]
            file_dict["template"] = f"{path}/{file_path}"

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

        # Configure Template Variables
        self.variables["name"] = name
        self.variables["name_simple"] = name.lower().replace(" ", "_").replace("-", "_")
        self.variables["description"] = description
        self.variables["maintainer"] = maintainer
        self.variables["contact"] = contact

        # Load the Template Config
        options = list(TEMPLATES.keys())
        template = promptUser("Select a TEMPLATE", options=options)
        template_name = TEMPLATES[template.capitalize()]
        if (template_name == "git"):
            url = promptUser("Enter Git Repo URL")
            template = self.__load_git_template(url)
        else:
            template = self.__load_template(template_name)

        # Prompt user based on the template
        for prompt in template.get("prompts", []):
            self.variables[prompt["var"]] = promptUser(prompt["message"])

        # Iterate over components for additional prompts and add any components that are scaffolded
        components = []
        componentFactory = ComponentFactory()
        for component in componentFactory.buildComponents():
            component = component.scaffold()
            if (component is not None):
                components.append(component)

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
                with open(file_dict["template"], "r", encoding="utf-8") as tmp_file:
                    with open(file_dict["name"], "w", encoding="utf-8") as dst_file:
                        dst_file.write(self.__format_variables(tmp_file.read()))

        print("Soldering the micro-computer to the skele-skull...")
        # Build the config object based on the user inputs
        cfg = self.__format_config(template["config"])
        cfg["name"] = name
        if "components" not in cfg:
            cfg["components"] = {}
        for component in components:
            component_dict = component.toDict()
            if component_dict != {}:
                cfg["components"][component.__class__.__name__.lower()] = component_dict

        config = Config.load(cfg)
        config.description = description
        config.maintainer = maintainer
        config.contact = contact
        config.version = "0.1.0"
        yaml.saveConfig(config)

        if (not self.existing):
            # Creating the files for the project
            print("Initializing default systems...")
            dockerfile.buildDockerfile(config)
            dockerignore.buildDockerignore(config)
            readme.buildREADME(config)

        print("Your Skelebot project is ready to go!")
