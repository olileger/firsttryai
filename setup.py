from setuptools import setup

"""
Note for the dumb creator of this CLI => In dev mode:
- pip install e .       # install the package in editable mode => TODO after each change into setup.py
- pip uninstall ftry    # remove the package from the environment
"""
setup(
    name="ftry",
    version="0.1",
    py_modules=["ftry"],
    entry_points={
        "console_scripts": [
            "ftry=ftry:main_sync",
            "yai=ftry:main_sync",
        ],
    },
)