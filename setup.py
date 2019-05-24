from setuptools import setup, find_packages

VERSION = '0.0.0'
with open('VERSION', 'r') as version:
    VERSION = version.read().replace("\n", "")

setup(
    name="skelebot",
    version=VERSION,
    description="ML Build Tool",
    author="Sean Shookman",
    author_email="sshookman@cars.com",
    packages=find_packages(),
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=[
        "pyyaml",
        "artifactory",
        "coverage",
        "pytest"
    ],
    install_requires=[
        "pyyaml",
        "artifactory",
        "coverage",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'skelebot = skelebot:main',
        ],
    }
)
