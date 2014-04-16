#!/usr/bin/env python

"""
test_clean

unittesting for pyinstaller module
"""

__version__ = "0.1.1"

import sys
import os
import unittest
import re

from setup_test_env import *
from distutilazy import pyinstaller
from distutils.dist import Distribution

class TestPyinstaller(unittest.TestCase):

    def test_finalize_opts(self):
        dist = Distribution()
        pi = pyinstaller.pyinstaller(dist)
        pi.target = 'fake.py'
        pi.finalize_options()
        self.assertTrue( re.match('.+', pi.name) )
        self.assertTrue(pi.pyinstaller_opts)

    def test_clean_all(self):
        dist = Distribution()
        cl = pyinstaller.clean_all(dist)
        cl.finalize_options()
        paths = cl.get_extra_paths()
        self.assertTrue(paths)
        spec = paths.pop()
        self.assertTrue( re.match('\S+\.spec', spec) )

if __name__ == '__main__':
    unittest.main()