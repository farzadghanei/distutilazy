"""
distutility.clean

commands to help clean files
"""

version = '0.2.1'

import os
import shutil
from distutils import log
from distutils.core import Command
from distutils.command import clean
import util

class clean_pyc(Command):
    description = """Clean root dir from complied python files"""
    user_options = [("root=", "r", "path to root dir")]

    def initialize_options(self):
        self.root = os.getcwd()
        self.extensions = 'pyc,pyo,pyd'

    def finalize_options(self):
        if not os.path.exists(self.root):
            raise IOError("Failed to access root path %s" % self.root)
        self.extensions = [ext.strip() for ext in self.extensions.split(',')]

    def find_compiled_files(self):
        """Find compiled Python files recursively in the root path

        :return: list of absolute file paths
        """
        files = []
        for ext in self.extensions:
            extfiles = util.find_files(self.root, "*.%s" % ext)
            log.debug("found %d .%s files in %s" % (len(extfiles), ext, self.root))
            files.extend(extfiles)
            del extfiles
        self.announce("found %d compiled python files in %s" % (len(files), self.root))
        return files

    def _clean_file(self, filename):
        """Clean a file if exists"""
        if not os.path.exists(filename):
            log.warn("'%s' does not exist -- can't clean it" % filename)
            return
        self.announce("removing %s" % filename)
        if not self.dry_run:
            os.remove(filename)

    def run(self):
        files = self.find_compiled_files()
        self.announce("cleaning compiled python files in %s ..." % self.root)
        if not self.dry_run:
            for filename in files:
                self._clean_file(filename)

class clean_all(clean.clean, clean_pyc):
    description = """Clean root dir from temporary files, complied files, etc."""

    def initialize_options(self):
        clean.clean.initialize_options(self)
        clean_pyc.initialize_options(self)

    def finalize_options(self):
        clean.clean.finalize_options(self)
        self.all = True
        clean_pyc.finalize_options(self)

    def get_egg_info_dir(self):
        return "%s.egg-info" % self.distribution.metadata.get_name()

    def _clean_dir(self, dirname):
        """Clean a directory if exists"""
        if not os.path.exists(dirname):
            log.warn("'%s' does not exist -- can't clean it" % dirname)
            return
        self.announce("cleaning %s" % dirname)
        if not self.dry_run:
            shutil.rmtree(dirname, True)

    def clean_egg_info(self):
        dirname = os.path.join(self.root, self.get_egg_info_dir())
        self._clean_dir(dirname)

    def clean_dist(self):
        self._clean_dir(os.path.join(self.root, 'dist'))

    def clean_build(self):
        self._clean_dir(os.path.join(self.root, 'build'))

    def run(self):
        clean.clean.run(self)
        clean_pyc.run(self)
        self.clean_egg_info()
        self.clean_dist()
        self.clean_build()
