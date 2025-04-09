from setuptools import setup, find_packages


#
# parse_requirements
#
# Read the requirements.txt file to pass along the dependencies to the setup function.
#
def parse_requirements(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip() and not line.startswith("#")]


#
# setup
#
# This function allows the creation of the CLI.
# Note for the dumb creator of this CLI => In dev mode:
# - pip install e .       # install the package in editable mode => TODO after each change into setup.py
# - pip uninstall ftry    # remove the package from the environment
#
setup(
    name="ftry",
    version="0.0.1",
    py_modules=["ftry"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ftry=ftry:main_sync",
            "yai=ftry:main_sync",
        ],
    },
    install_requires=parse_requirements("requirements.txt"),
)