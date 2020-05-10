"""Setup script for htooldeploy"""
import os
import sys

from setuptools import setup

sys.path.append(os.path.abspath("."))

setup(
    name="htooldeploy",
    version=__import__("htooldeploy").__version__,
    packages=["htooldeploy"],
    entry_points={
        "console_scripts": [
            "htooldeploy = htooldeploy.__main__:main"
        ]
    }
)
