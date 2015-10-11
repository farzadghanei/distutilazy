"""
distutilazy.clean
-----------------

command classes to help clean temporary files

:license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import os
from shutil import rmtree
from distutils import log
from distutils.core import Command
from distutils.command import clean

from . import util

__version__ = "0.4.0"


class CleanPyc(Command):
    description = """Clean root dir from complied python files"""
    user_options = [("root=", "r", "path to root dir")]

    def initialize_options(self):
        self.root = os.getcwd()
        self.extensions = "pyc,pyo,pyd"
        self.directories = "__pycache__,"

    def finalize_options(self):
        if not os.path.exists(self.root):
            raise IOError("Failed to access root path '{}'".format(self.root))
        self.extensions = [ext.strip() for ext in self.extensions.split(',')]
        self.directories = [dir.strip() for dir in self.directories.split(',')]

    def find_compiled_files(self):
        """Find compiled Python files recursively in the root path

        :return: list of absolute file paths
        """
        files = []
        for ext in self.extensions:
            ext_files = util.find_files(self.root, "*." + ext)
            log.debug("found {} '.{}' files in '{}'".format(
                len(ext_files), ext, self.root)
            )
            files.extend(ext_files)
        self.announce("found '{}' compiled python files in '{}'".format(
            len(files), self.root))
        return files

    def find_cache_directories(self):
        directories = []
        for dir_name in self.directories:
            dirs = util.find_directories(self.root, dir_name)
            log.debug("found {} directories in '{}'".format(
                len(dirs), self.root))
            directories.extend(dirs)
        self.announce("found {} python cache directories in '{}'".format(
            len(directories), self.root))
        return directories

    def _clean_file(self, filename):
        """Clean a file if exists and not in dry run"""
        if not os.path.exists(filename):
            return
        self.announce("removing '{}'".format(filename))
        if not self.dry_run:
            os.remove(filename)

    def _clean_directory(self, name):
        """Clean a directory if exists and not in dry run"""
        if not os.path.exists(name):
            return
        self.announce(
            "removing directory '{}' and all its contents".format(name)
        )
        if not self.dry_run:
            rmtree(name, True)

    def run(self):
        directories = self.find_cache_directories()
        if directories:
            self.announce(
                "cleaning python cache directories in '{}' ...".format(
                    self.root))
            if not self.dry_run:
                for dir_name in directories:
                    self._clean_directory(dir_name)

        files = self.find_compiled_files()
        if files:
            self.announce(
                "cleaning compiled python files in '{}' ...".format(self.root))
            if not self.dry_run:
                for filename in files:
                    self._clean_file(filename)


class CleanAll(clean.clean, CleanPyc):
    description = "Clean root dir from temporary files (complied files, etc)"
    user_options = [
        ("keep-build", None, "do not clean build directory"),
        ("keep-dist", None, "do not clean dist directory"),
        ("keep-egginfo", None, "do not clean egg info directory"),
        ("keep-extra", None, "do not clean extra files"),
    ]

    boolean_options = ["keep-build", "keep-dist", "keep-egginfo", "keep-extra"]

    def initialize_options(self):
        clean.clean.initialize_options(self)
        CleanPyc.initialize_options(self)
        self.keep_build = None
        self.keep_dist = None
        self.keep_egginfo = None
        self.keep_extra = None

    def finalize_options(self):
        clean.clean.finalize_options(self)
        CleanPyc.finalize_options(self)
        self.all = True

    def get_egginfo_dir(self):
        return self.distribution.metadata.get_name() + ".egg-info"

    def get_extra_paths(self):
        """Return list of extra files/directories to be removed"""
        return []

    def clean_egginfo(self):
        """Clean .egginfo directory"""
        dir_name = os.path.join(self.root, self.get_egginfo_dir())
        self._clean_directory(dir_name)

    def clean_dist(self):
        self._clean_directory(os.path.join(self.root, "dist"))

    def clean_build(self):
        self._clean_directory(os.path.join(self.root, "build"))

    def clean_extra(self):
        """Clean extra files/directories specified by get_extra_paths()"""
        extra_paths = self.get_extra_paths()
        for path in extra_paths:
            if not os.path.exists(path):
                continue
            if os.path.isdir(path):
                self._clean_directory(path)
            else:
                self._clean_file(path)

    def run(self):
        clean.clean.run(self)
        CleanPyc.run(self)
        if not self.keep_build:
            self.clean_build()
        if not self.keep_egginfo:
            self.clean_egginfo()
        if not self.keep_dist:
            self.clean_dist()
        if not self.keep_extra:
            self.clean_extra()

clean_pyc = CleanPyc
clean_all = CleanAll