"""
    distutilazy.tests.test_util
    -----------------

    Test distutilazy.util module.

    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

__version__ = "0.1.0"

import os
from os import path
import sys
import unittest

from .setup_test_env import *
from distutilazy import util

class TestUtil(unittest.TestCase):

    def test_util_find_files(self):
        me = os.path.realpath(__file__)
        files = util.find_files(TEST_DIR, "test_util.py*")
        self.assertTrue(me in files)
        files = util.find_files(TEST_DIR, "not_existing_file.py")
        self.assertEqual(files, [])
