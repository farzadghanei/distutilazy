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
        ("pyinstaller-path=", None, "path to pyinstaller executable")
    ]

    def initialize_options(self):
        self.pyinstaller_path = None
        self.pyinstaller_options = None

    def get_pyinstaller_bin(self):
        """Return path to pyinstaller executable"""
        pi = 'pyinstaller'
        if self.pyinstaller_path:
            pi = os.path.join(self.pyinstaller_path, pi)
        return pi

    def default_pyinstaller_opts(self):
        """Return default options for PyInstaller.
        Use this method to customize the command for separate projects

        :return: list of options
        """
        return []

    def finalize_options(self):
        if self.pyinstaller_path:
            self.pyinstaller_path = os.path.abspath(self.pyinstaller_path)
            if not os.path.exists(self.get_pyinstaller_bin()):
                raise DistutilsOptionError("failed to find pyinstaller in %s" % self.pyinstaller_path)
        self.pyinstaller_options = self._default_pyinstaller_opts()

    def run(self):
        pi = self._get_pyinstaller_bin()
        opts = self.pyinstaller_options
        self.announce("running %s %s" % (pi, ' '.join(opts)))
        code = subprocess.call(pi, opts)
        return code

class clean_all(clean.clean_all):
    """Distutils command to clean all temporary files, compiled Python files, PyInstaller temp files and spec."""

    def initialize_options(self):
        clean.clean_all.initialize_options(self)
        self.spec_file = None

    def finalize_options(self):
        clean.clean_all.finalize_options(self)
        if not self.spec_file:
            self.spec_file = "%s.spec" % self.distribution.metadata.get_name()

    def clean_spec(self):
        self._clean_file(self.spec_file)

    def run(self):
        clean.clean_all.run(self)
        self.clean_spec()
