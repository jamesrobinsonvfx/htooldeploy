"""Setup script for htooldeploy"""
import os
import sys

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

sys.path.append(os.path.abspath("."))

setup(
    name="htooldeploy",
    version=__import__("htooldeploy").__version__,
    packages=["htooldeploy"],
    entry_points={
        "console_scripts": [
            "htooldeploy = htooldeploy.__main__:main"
        ]
    },
    install_requires=[],
    author="James Robinson",
    author_email="james@jamesrobinsonvfx.com",
    description="Command line application for installing Houdini tools.",
    long_description=long_description,
    long_description_content_type="test/markdow",
    url="https://github.com/jamesrobinsonvfx/htooldeploy",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    python_requires=">=2.7,<=3.0",
    keywords=["houdini"],
    license="MIT",
    project_urls={
        "Documentation": "https://htooldeploy.readthedocs.io/en/latest/",
        "GitHub": "https://github.com/jamesrobinsonvfx/htooldeploy"
    }
)
