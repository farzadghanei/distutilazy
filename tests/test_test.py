"""
distutilazy.tests.test_test
----------------------------

Tests for distutilazy.test module

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import sys
from os.path import dirname, basename
from os.path import join as path_join
from distutils.dist import Distribution
from unittest import TestCase, TestSuite, main, skip

HERE = dirname(__file__)
sys.path.insert(0, dirname(HERE))
sys.path.insert(0, HERE)

from distutilazy.test import RunTests, test_suite_for_modules

__file__ = basename(__file__[:-1] if __file__.endswith('.pyc') else __file__)
FIXTURES = path_join(path_join(dirname(__file__), 'fixtures'), 'test_test')


def get_module_names(modules):
    return map(lambda m: m.__name__, modules)


class TestTest(TestCase):

    def test_find_modules_from_package_path(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_package_path(HERE)
        self.assertIn('tests.test_test', get_module_names(modules))

    def test_get_modules_from_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        self.assertEqual(
            [], test_runner.get_modules_from_files(['none_existing_file']))
        modules = test_runner.get_modules_from_files([__file__])
        self.assertEqual(1, len(modules))
        self.assertEqual('test_test', modules.pop().__name__)

    def test_find_test_modules_from_test_files(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        modules = test_runner.find_test_modules_from_test_files(
            HERE, 'none_exiting_pattern')
        self.assertEqual([], modules)
        modules = test_runner.find_test_modules_from_test_files(HERE, __file__)
        self.assertEqual(1, len(modules))
        self.assertEqual('tests.test_test', modules.pop().__name__)
        modules = test_runner.find_test_modules_from_test_files(HERE, 'test_*')
        module_names = get_module_names(modules)
        self.assertIn('tests.test_test', module_names)
        self.assertIn('subdir.test_subdir', module_names)

    def test_test_suite_for_modules(self):
        self.assertIsInstance(test_suite_for_modules([]), TestSuite)

    def test_get_test_runner(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        runner = test_runner.get_test_runner()
        self.assertTrue(hasattr(runner, 'run'))
        self.assertTrue(hasattr(runner.run, '__call__'))

    def test_get_modules_from_files_raises_import_error_if_any(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        filename = path_join(FIXTURES, "hasimporterr.py")
        self.assertRaises(ImportError, test_runner.get_modules_from_files, [filename])

    def test_find_test_modules_from_test_files_raises_import_error(self):
        dist = Distribution()
        test_runner = RunTests(dist)
        test_runner.finalize_options()
        self.assertRaises(ImportError,
                test_runner.find_test_modules_from_test_files,
                HERE, 'hasimporterr*')


if __name__ == '__main__':
    main()
