"""
distutilazy.tests.test_test
----------------------------

Tests for distutilazy.test module

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

from os.path import dirname, basename
import sys
import unittest

sys.path.insert(0, dirname(dirname(__file__)))
sys.path.insert(0, dirname(__file__))

from distutilazy import test
from distutils.dist import Distribution

# if running in a cached compiled python file
# assume filename as python source file.
# when tests are running together, test_clean
# removes pyc files. but .py file will be available
_me_ = basename(__file__[:-1] if __file__.endswith('.pyc') else __file__)

if __file__[-1].lower() == 'c':
    __file__ = __file__[:-1]


def get_module_py_file_names(modules):
    return map(
            lambda name: name[:-1] if name.endswith('.pyc') else name,
            map(lambda m: basename(m.__file__), modules)
        )


class TestTest(unittest.TestCase):

    def test_find_modules_from_package_path(self):
        dist = Distribution()
        test_runner = test.run_tests(dist)
        test_runner.finalize_options()
        here = dirname(__file__)
        modules = test_runner.find_test_modules_from_package_path(here)
        self.assertIn(_me_, get_module_py_file_names(modules))

    def test_get_modules_from_files(self):
        dist = Distribution()
        test_runner = test.run_tests(dist)
        test_runner.finalize_options()
        self.assertEqual(
            [], test_runner.get_modules_from_files(['none_existing_file']))
        modules = test_runner.get_modules_from_files([_me_])
        self.assertEqual(1, len(modules))
        self.assertEqual(_me_, basename(modules.pop().__file__))

    def test_find_test_modules_from_test_files(self):
        dist = Distribution()
        test_ = test.run_tests(dist)
        test_.finalize_options()
        here = dirname(__file__)
        filename = basename(__file__)
        modules = test_.find_test_modules_from_test_files(here, 'none_exiting_pattern')
        self.assertEqual([], modules)
        modules = test_.find_test_modules_from_test_files(here, filename)
        self.assertEqual(1, len(modules))
        self.assertEqual(filename, basename(modules.pop().__file__))
        modules = test_.find_test_modules_from_test_files(here, 'test_*')
        module_names = get_module_py_file_names(modules)
        self.assertIn(filename, module_names)
        self.assertIn('test_subdir.py', module_names)

    def test_test_suite_for_modules(self):
        dist = Distribution()
        test_ = test.run_tests(dist)
        test_.finalize_options()
        suite = test_.test_suite_for_modules([])
        self.assertIsInstance(suite, unittest.TestSuite)

    def test_get_test_runner(self):
        dist = Distribution()
        test_ = test.run_tests(dist)
        test_.finalize_options()
        runner = test_.get_test_runner()
        self.assertTrue(hasattr(runner, 'run'))
        self.assertTrue(hasattr(runner.run, '__call__'))

if __name__ == '__main__':
    unittest.main()
