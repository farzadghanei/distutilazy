"""

    distutilazy.clean
    -----------------

    command classes to help clean temporary files

    :license: MIT, see LICENSE for more details.

"""

__version__ = "0.2.4"

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
        self.extensions = "pyc,pyo,pyd"

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
    user_options = [
        ("keep-build", None, "do not clean build direcotry"),
        ("keep-dist", None, "do not clean dist direcotry"),
        ("keep-egginfo", None, "do not clean egg info direcotry"),
        ("keep-extra", None, "do not clean extra files"),
    ]

    boolean_options = ["keep-build", "keep-dist", "keep-egginfo", "keep-extra"]

    def initialize_options(self):
        clean.clean.initialize_options(self)
        clean_pyc.initialize_options(self)
        self.keep_build = None
        self.keep_dist = None
        self.keep_egginfo = None
        self.keep_extra = None

    def finalize_options(self):
        clean.clean.finalize_options(self)
        clean_pyc.finalize_options(self)
        self.all = True

    def get_egginfo_dir(self):
        return "%s.egg-info" % self.distribution.metadata.get_name()

    def _clean_dir(self, dirname):
        """Clean a directory if exists"""
        if not os.path.exists(dirname):
            log.warn("'%s' does not exist -- can't clean it" % dirname)
            return
        self.announce("cleaning %s" % dirname)
        if not self.dry_run:
            shutil.rmtree(dirname, True)

    def get_extra_paths(self):
        """Return list of extra files/directories to be removed"""
        return []

    def clean_egginfo(self):
        """Clean .egginfo directory"""
        dirname = os.path.join(self.root, self.get_egginfo_dir())
        self._clean_dir(dirname)

    def clean_dist(self):
        self._clean_dir(os.path.join(self.root, "dist"))

    def clean_build(self):
        self._clean_dir(os.path.join(self.root, "build"))

    def clean_extra(self):
        """Clean extra files/directories specified by get_extra_paths()"""
        extra_paths = self.get_extra_paths()
        for path in extra_paths:
            if not os.path.exists(path):
                log.warn("'%s' does not exist -- can't clean it" % path)
                continue
            if os.path.isdir(path):
                self._clean_dir(path)
            else:
                self._clean_file(path)

    def run(self):
        clean.clean.run(self)
        clean_pyc.run(self)
        if not self.keep_build:
            self.clean_build()
        if not self.keep_egginfo:
            self.clean_egginfo()
        if not self.keep_dist:
            self.clean_dist()
        if not self.keep_extra:
            self.clean_extra()
