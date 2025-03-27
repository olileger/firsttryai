from setuptools import setup

setup(
    name="ftry",
    version="0.1",
    py_modules=["ftry"],
    entry_points={
        "console_scripts": [
            "ftry=ftry:main",
            "yai=ftry:main",
        ],
    },
)