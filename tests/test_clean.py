#!/usr/bin/env python

"""
test_clean

unittesting for clean module
"""

__version__ = "0.2.0"

import sys
import os
import unittest

from setup_test_env import *
from distutilazy import clean
from distutils.dist import Distribution

class TestClean(unittest.TestCase):

    def test_clean_all(self):
        dist = Distribution()
        dist.metadata.name = 'testdist'
        cl = clean.clean_all(dist)
        cl.finalize_options()
        self.assertEquals(cl.get_egginfo_dir(), 'testdist.egg-info')
        targets = ['build', 'dist', 'egginfo', 'extra']
        bad_calls = []
        good_calls = []
        good_calls_should_be = 0
        for target in targets:
            cl = clean.clean_all(dist)
            cl.finalize_options()
            cl.dry_run = True
            setattr(cl, 'keep_%s' % target, True)
            setattr(cl, 'clean_%s' % target, lambda self: bad_calls.append(targt))
            other_targets = [t for t in targets if t != target]
            for ot in other_targets:
                good_calls_should_be += 1
                setattr(cl, 'clean_%s' % ot, lambda self=None: good_calls.append(ot))
            cl.run()
        self.assertEquals(bad_calls, [])
        self.assertEquals(len(good_calls), good_calls_should_be)

    def test_clean_pyc(self):
        dist = Distribution()
        cl = clean.clean_pyc(dist)
        cl.extensions = 'ppyycc, ppyyoo'
        cl.finalize_options()
        self.assertEquals(cl.extensions, ['ppyycc', 'ppyyoo'])
        self.assertEquals(cl.find_compiled_files(), [])

if __name__ == '__main__':
    unittest.main()
