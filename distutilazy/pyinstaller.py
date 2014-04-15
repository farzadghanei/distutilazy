"""
distutility.clean

helper commands for using pyinstaller
"""

version = '0.1.0'

import os
from distutils.core import Command
from distutils.errors import DistutilsOptionError
import clean

class pyinstaller(Command):
    """Distutils command to run PyInstaller with configured defaults"""

    description = """Run PyInstaller to compile standalone binary executables"""

    user_options = [
        ("pyinstaller=", None, "path to pyinstaller executable"),
        ("name", None, "name of the bundled app")
    ]

    def initialize_options(self):
        self.pyinstaller_path = None
        self.name = None
        self.pyinstaller_opts = None

    def default_pyinstaller_opts(self):
        """Return default options for PyInstaller.
        Use this method to customize the command for separate projects

        :return: list of options
        """
        return []

    def finalize_options(self):
        if self.pyinstaller_path:
            self.pyinstaller_path = os.path.abspath(self.pyinstaller_path)
            if not os.path.exists(self.pyinstaller_path):
                raise DistutilsOptionError("failed to find pyinstaller from %s" % self.pyinstaller_path)
        self.pyinstaller_opts = self.default_pyinstaller_opts()
        if not self.name:
            self.name = self.distribution.metadata.get_name()
        self.pyinstaller_opts.append('--name=%s' % self.name)

    def run(self):
        pi = self.pyinstaller_path
        opts = self.pyinstaller_opts
        self.announce("running %s %s" % (pi, ' '.join(opts)))
        code = subprocess.call(pi, opts)
        return code

class clean_all(clean.clean_all):
    """Distutils command to clean all temporary files, compiled Python files, PyInstaller temp files and spec."""

    user_options = [
        ("keep-build", None, "do not clean build direcotry"),
        ("keep-dist", None, "do not clean dist direcotry"),
        ("keep-egginfo", None, "do not clean egg info direcotry"),
        ("keep-extra", None, "do not clean extra files"),
        ("name", None, "name of the bundled app"),
    ]

    def initialize_options(self):
        clean.clean_all.initialize_options(self)
        self.name = None

    def finalize_options(self):
        clean.clean_all.finalize_options(self)
        if not self.name:
            self.name = self.distribution.metadata.get_name()

    def get_extra_paths(self):
        """Return list of extra files/directories to be removed"""
        return ["%s.spec" % self.name]
