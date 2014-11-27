#!/usr/bin/env python

"""

distutilazy
===========

Extra distutils commands.

License
-------
Distutilazy is released under the terms of `MIT license <http://opensource.org/licenses/MIT>`_.

"""

from __future__ import print_function

import os
import sys

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError as exp:
    print("using distutils. install setuptools for more options", file=sys.stderr)
    setuptools = None
    from distutils.core import setup

import distutilazy
import distutilazy.clean

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Archiving :: Packaging",
    "Topic :: System :: Systems Administration",
]

long_description = __doc__
with open(os.path.join(os.path.dirname(__file__), "README.rst")) as fh:
    long_description = fh.read()

params = dict(
    name = "distutilazy",
    author = "Farzad Ghanei",
    author_email = "farzad.ghanei@gmail.com",
    url = "http://github.com/farzadghanei/distutilazy/",
    packages = setuptools and find_packages() or ["distutilazy", "tests"],
    version = distutilazy.__version__,
    description = "Extra distutils commands",
    long_description = long_description,
    license = "MIT",
    classifiers = CLASSIFIERS,
    cmdclass = {"clean_pyc": distutilazy.clean.clean_pyc, "clean_all": distutilazy.clean.clean_all}
)

if setuptools:
    params.update(
        zip_safe = False,
        test_suite = "tests",
    )

dist = setup(**params)
