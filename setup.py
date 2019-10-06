from setuptools import setup, find_packages

VERSION = '0.0.0'
with open('VERSION', 'r') as version:
    VERSION = version.read().replace("\n", "")

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="skelebot",
    version=VERSION,
    description="ML Build Tool",
    author="Sean Shookman",
    author_email="sshookman@cars.com",
    packages=find_packages(),
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=requirements,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'skelebot = skelebot:main',
        ],
    }
)
