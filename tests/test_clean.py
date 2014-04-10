#!/usr/bin/env python

"""
test_clean

unittesting for clean module
"""

__version__ = "0.1.0"

import sys
import os
import unittest

from setup_test_env import *
from distutilazy import clean
from distutils.dist import Distribution

class TestCommon(unittest.TestCase):

    def test_clean_pyc(self):
        dist = Distribution()
        cl = clean.clean_pyc(dist)
        cl.initialize_options()
        cl.extensions = 'ppyycc, ppyyoo'
        cl.finalize_options()
        self.assertEquals(cl.extensions, ['ppyycc', 'ppyyoo'])
        self.assertEquals(cl.find_compiled_files(), [])

if __name__ == '__main__':
    unittest.main()
