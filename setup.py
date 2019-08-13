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
        "PyYAML==5.1.2",
        "artifactory==0.1.17",
        "requests==2.22.0",
        "schema==0.7.0",
        "coverage",
        "pytest"
    ],
    install_requires=[
        "PyYAML==5.1.2",
        "artifactory==0.1.17",
        "requests==2.22.0",
        "schema==0.7.0",
        "coverage",
        "pytest"
    ],
    entry_points={
        'console_scripts': [
            'skelebot = skelebot:main',
        ],
    }
)
