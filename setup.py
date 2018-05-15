#!/usr/bin/env python
from spectre import __version__
from setuptools import setup, find_packages

setup(name="spectre",
    version=__version__,
    description="",
    author="ADS",
    author_email="imss-ads-staff@caltech.edu",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "htmlcov"])
    )
