#!/usr/bin/env python

import os
import sys
import importlib
import unittest
import getopt

import tests

def usage():
    return """Runs unit tests.
By default runs all unit tests, but you may specify which tests to run
by passing their names (module or file name) as arguments.

Usage: {0} [opts] [test1] [test2] ...

Options
    -h, --help          show this help and exit
    -v, --verbose       output more messages

    """.format(__file__)

def main(opts, args):
    verbose = False

    for k, v in opts:
        if k in ('-h', '--help'):
            print(usage())
            return getattr(os, 'EX_OK', 0)
        if k in ('-v', '--verbose'):
            verbose = True

    def out(msg):
        if verbose:
            print(msg)

    mod_names = args or tests.test_modules
    suite = unittest.TestSuite()
    for mod_name in mod_names:
        out("importing {0} ...".format(mod_name))
        mod = importlib.import_module("tests." + mod_name)
        mod_tests = unittest.defaultTestLoader.loadTestsFromModule(mod)
        suite.addTests(mod_tests)
    out("running tests ...")
    unittest.TextTestRunner(verbosity=(2 if verbose else 1)).run(suite)
    return getattr(os, 'EX_OK', 0)

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "verbose"])
    sys.exit(main(opts, args))

