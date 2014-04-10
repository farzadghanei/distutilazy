# This file is part of distutilazy released under the MIT license.
# See the LICENSE for more information.

import os
import shutil
from distutils import log
from distutils.core import Command
from distutils.command import clean
import common

class clean_pyc(Command):
    description = """Clean root dir from complied python files"""
    user_options = [("root", "r", "path to root dir")]

    def initialize_options(self):
        self.root = os.getcwd()
        self.extensions = 'pyc,pyo,pyd'

    def finialize_options(self):
        if not os.path.exists(self.root):
            raise IOError("Failed to access root path %s" % self.root)
        self.extensions = [ext.strip() for ext in self.extensions.split(',')]

    def find_compiled_files(self):
        """Finds compiled Python files recursively in the root path

        :returns: list of absolute file paths
        """
        files = []
        for ext in self.extensions:
            extfiles = common.find_files(self.root, "*.%s" % ext)
            log.debug("found %d .%s files in %s" % (len(extfiles), ext, self.root))
            files.extend(extfiels)
            del extfiles
        log.info("found %d compiled python files in %s" % (len(files), self.root))
        return files

    def run(self):
        files = self.find_compiled_files()
        log.info("cleaning compiled python files in %s ..." % self.root)
        for file_ in files:
            log.debug("removing %s " % file_)
            os.remove(file_)

class clean_all(clean.clean, clean_pyc):
    description = """Clean root dir from temporary files, complied files, etc."""

    def run(self):
        clean.clean.run(self)
        clean_pyc.run(self)
        for d in ['dist', 'build']:
            path = os.path.join(self.root, d)
            if os.path.exists(path):
                shutil.rmtree(path, True)
