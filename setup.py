#!/usr/bin/env python

# This file is part of distutilazy released under the MIT license.
# See the LICENSE for more information.

import os
import sys

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print >> sys.strerr, "using distutils. install setuptools for more options"
    setuptools = None
    from distutils.core import setup

import distutilazy

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Archiving :: Packaging',
    'Topic :: System :: Systems Administration',
    'Topic :: Utilities'
]

long_description = "Extra distutils commands"
# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.rst') as fh:
    long_description = fh.read()

params = dict(
    name = APP_NAME,
    packages = setuptools and find_packages() or ['distutilazy', 'tests'],
    version = __version__,
    description = "Extra distutils commands",
    long_description = long_description,
    license = 'MIT',
    classifiers = CLASSIFIERS,
    cmdclass = {"clean_py": distutilazy.clean.clean_py, "clean_all": distutilazy.clean.clean_all}
)

if setuptools:
    params.update(
        zip_safe = True,
        test_suite = 'tests',
    )

setup(**params)
