"""
distutilazy.tests.test_test
----------------------------

Tests for distutilazy.test module

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from os.path import dirname, basename
import sys
from distutils.dist import Distribution
from unittest import TestCase, TestSuite, main

here = dirname(__file__)
sys.path.insert(0, dirname(here))
sys.path.insert(0, here)

from distutilazy.test import RunTests, test_suite_for_modules

__file__ = basename(__file__[:-1] if __file__.endswith('.pyc') else __file__)


def get_module_py_file_names(modules):
    return map(
            lambda name: name[:-1] if name.endswith('.pyc') else name,
            map(lambda m: basename(m.__file__), modules)
        )


class TestTest(TestCase):

    def test_find_modules_from_package_path(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_package_path(here)
        self.assertIn(__file__, get_module_py_file_names(modules))

    def test_get_modules_from_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        self.assertEqual(
            [], test_runner.get_modules_from_files(['none_existing_file']))
        modules = test_runner.get_modules_from_files([__file__])
        self.assertEqual(1, len(modules))
        self.assertEqual(__file__, basename(modules.pop().__file__))

    def test_find_test_modules_from_test_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_test_files(
            here, 'none_exiting_pattern')
        self.assertEqual([], modules)
        modules = test_runner.find_test_modules_from_test_files(here, __file__)
        self.assertEqual(1, len(modules))
        self.assertEqual(__file__, basename(modules.pop().__file__))
        modules = test_runner.find_test_modules_from_test_files(here, 'test_*')
        module_names = get_module_py_file_names(modules)
        self.assertIn(__file__, module_names)
        self.assertIn('test_subdir.py', module_names)

    def test_test_suite_for_modules(self):
        self.assertIsInstance(test_suite_for_modules([]), TestSuite)

    def test_get_test_runner(self):
        dist = Distribution()
        test_ = RunTests(dist)
        test_.finalize_options()
        runner = test_.get_test_runner()
        self.assertTrue(hasattr(runner, 'run'))
        self.assertTrue(hasattr(runner.run, '__call__'))

if __name__ == '__main__':
    main()