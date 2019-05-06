import os
import yaml
from setuptools import setup, find_packages

cwd = os.getcwd()
config = None
cfgFile = "{path}/skelebot.yaml".format(path=cwd)
if os.path.isfile(cfgFile):
    with open(cfgFile, 'r') as stream:
        config = yaml.load(stream)

setup(
    name=config["name"],
    version=config["version"],
    description=config["description"],
    author=config["maintainer"],
    author_email=config["contact"],
    packages=find_packages(),
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=config["components"]["dependencies"],
    install_requires=config["components"]["dependencies"],
    entry_points={
        'console_scripts': [
            'skelebot = skelebot:main',
        ],
    }
)
