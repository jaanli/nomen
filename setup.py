#!/usr/bin/env python
# setup
# Setup script for installing nomen

##########################################################################
## Imports
##########################################################################

import os
import re
import codecs

from setuptools import setup
from setuptools import find_packages

##########################################################################
## Package Information
##########################################################################

## Basic information
NAME = "nomen"
DESCRIPTION = "YAML configuration tree with command line flags."
AUTHOR = "Jaan Altosaar"
EMAIL = "j@jaan.io"
LICENSE = "MIT"
REPOSITORY = "https://github.com/altosaar/nomen"
PACKAGE = "nomen"

## Define the keywords
KEYWORDS = (
    'nomen', 'python', 'option', 'tree', 'nested', 'dict', 'parameter', 'flags'
)

## Define the classifiers
## See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
)

## Important Paths
PROJECT = os.path.abspath(os.path.dirname(__file__))
VERSION_PATH = os.path.join(PACKAGE, "version.py")

## Directories to ignore in find_packages
EXCLUDES = (
    "tests", "bin", "docs", "fixtures", "register", "notebooks",
)

## Requirements
REQUIREMENTS = ["pyyaml", "addict"]

##########################################################################
## Helper Functions
##########################################################################


def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts), 'rb', 'utf-8') as f:
        return f.read()


def get_version(path=VERSION_PATH):
    """
    Reads the version.py defined in the VERSION_PATH to find the get_version
    function, and executes it to ensure that it is loaded correctly.
    """
    namespace = {}
    exec(read(path), namespace)
    return namespace['get_version']()


##########################################################################
## Define the configuration
##########################################################################

config = {
    "name": NAME,
    "version": get_version(),
    "description": DESCRIPTION,
    "long_description": DESCRIPTION,
    "license": LICENSE,
    "author": AUTHOR,
    "author_email": EMAIL,
    "maintainer": AUTHOR,
    "maintainer_email": EMAIL,
    "url": REPOSITORY,
    "download_url": "{}/tarball/v{}".format(REPOSITORY, get_version()),
    "packages": find_packages(where=PROJECT, exclude=EXCLUDES),
    "classifiers": CLASSIFIERS,
    "keywords": KEYWORDS,
    "zip_safe": False,
    "install_requires": REQUIREMENTS,
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
