#!/usr/bin/env python

"""
test_util

unittesting for util module
"""

__version__ = "0.1.0"

import sys
import os
import unittest

from setup_test_env import *
from distutilazy import util

class TestUtil(unittest.TestCase):

    def test_util_find_files(self):
        me = os.path.realpath(__file__)
        files = util.find_files(TEST_DIR, 'test_util.py*')
        self.assertTrue(me in files)
        files = util.find_files(TEST_DIR, 'not_existing_file.py')
        self.assertEqual(files, [])

if __name__ == '__main__':
    unittest.main()
