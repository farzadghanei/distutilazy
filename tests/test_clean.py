"""
distutilazy.tests.test_clean
----------------------------

Tests for distutilazy.clean module
"""

from __future__ import absolute_import

import sys
from shutil import rmtree
from os import path, mkdir
from os.path import dirname, abspath
from unittest import TestCase, main
from distutils.dist import Distribution

here = dirname(__file__)
sys.path.insert(0, dirname(here))
sys.path.insert(0, here)

from distutilazy import clean


class TestClean(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_cache_dir = abspath(path.join(here, '_test_py_cache_'))
        if path.exists(cls.test_cache_dir):
            raise Exception(
                    "Test python cache directory exists in '{}'." \
                    " Please remove this path".format(cls.test_cache_dir)
                    )
        mkdir(cls.test_cache_dir)

    @classmethod
    def tearDownAfter(cls):
        if path.exists(cls.test_cache_dir):
            rmtree(cls.test_cache_dir, True)

    def test_clean_all(self):
        dist = Distribution()
        dist.metadata.name = "test_dist"
        clean_dist = clean.clean_all(dist)
        clean_dist.finalize_options()
        self.assertEqual(clean_dist.get_egginfo_dir(), "test_dist.egg-info")
        targets = ["build", "dist", "egginfo", "extra"]
        bad_calls = []
        good_calls = []
        good_calls_should_be = 0
        for target in targets:
            clean_dist = clean.clean_all(dist)
            clean_dist.finalize_options()
            clean_dist.dry_run = True
            setattr(clean_dist, "keep_%s" % target, True)
            setattr(clean_dist, "clean_%s" % target,
                    lambda x: bad_calls.append(target))
            other_targets = [t for t in targets if t != target]
            for other_target in other_targets:
                good_calls_should_be += 1
                setattr(clean_dist, "clean_%s" % other_target,
                        lambda x=None: good_calls.append(other_target))
            clean_dist.run()
        self.assertEqual(bad_calls, [])
        self.assertEqual(len(good_calls), good_calls_should_be)

    def test_clean_pyc(self):
        dist = Distribution()
        pyc_cleaner = clean.clean_pyc(dist)
        pyc_cleaner.extensions = "ppyycc, ppyyoo"
        pyc_cleaner.finalize_options()
        self.assertEqual(pyc_cleaner.extensions, ["ppyycc", "ppyyoo"])
        self.assertEqual(pyc_cleaner.find_compiled_files(), [])

    def test_clean_py_cache_dirs(self):
        dist = Distribution()
        pycache_cleaner = clean.clean_pyc(dist)
        pycache_cleaner.directories = "_test_py_cache_"
        pycache_cleaner.finalize_options()
        self.assertEqual(pycache_cleaner.directories, ["_test_py_cache_"])
        self.assertEqual(
            pycache_cleaner.find_cache_directories(),
            [self.__class__.test_cache_dir]
        )
        pycache_cleaner.run()
        self.assertFalse(path.exists(self.__class__.test_cache_dir))

    def test_clean_py_cache_dirs_finds_nothing(self):
        dist = Distribution()
        pycache_cleaner = clean.clean_pyc(dist)
        pycache_cleaner.extensions = "ppyycc, ppyyoo"
        pycache_cleaner.directories = "not_exist, and_not_found"
        pycache_cleaner.finalize_options()
        self.assertEqual(
            pycache_cleaner.directories,
            ["not_exist", "and_not_found"]
        )
        self.assertEqual(pycache_cleaner.find_cache_directories(), [])

if __name__ == "__main__":
    main()