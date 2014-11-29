"""
    distutilazy.tests.test_clean
    ----------------------------

    Tests for distutilazy.clean module

    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

__version__ = "0.3.0"

import sys
import os
import unittest

from .setup_test_env import *
from distutilazy import clean
from distutils.dist import Distribution

class TestClean(unittest.TestCase):

    def test_clean_all(self):
        dist = Distribution()
        dist.metadata.name = "testdist"
        cl = clean.clean_all(dist)
        cl.finalize_options()
        self.assertEqual(cl.get_egginfo_dir(), "testdist.egg-info")
        targets = ["build", "dist", "egginfo", "extra"]
        bad_calls = []
        good_calls = []
        good_calls_should_be = 0
        for target in targets:
            cl = clean.clean_all(dist)
            cl.finalize_options()
            cl.dry_run = True
            setattr(cl, "keep_%s" % target, True)
            setattr(cl, "clean_%s" % target, lambda self: bad_calls.append(targt))
            other_targets = [t for t in targets if t != target]
            for ot in other_targets:
                good_calls_should_be += 1
                setattr(cl, "clean_%s" % ot, lambda self=None: good_calls.append(ot))
            cl.run()
        self.assertEqual(bad_calls, [])
        self.assertEqual(len(good_calls), good_calls_should_be)

    def test_clean_pyc(self):
        dist = Distribution()
        cl = clean.clean_pyc(dist)
        cl.extensions = "ppyycc, ppyyoo"
        cl.finalize_options()
        self.assertEqual(cl.extensions, ["ppyycc", "ppyyoo"])
        self.assertEqual(cl.find_compiled_files(), [])
