"""
distutility.pyinstaller

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
        ("target=", None, "Taget Python app to bundle"),
        ("pyinstaller=", None, "Path to pyinstaller executable"),
        ("name=", "n", "Name of the bundled app"),
        ("one-file", "F", "Create a one-file bundled executable"),
        ("icon=", "i", "Path to icon resource"),
        ("windowed=", "w", "Windowed app, no console for stdio"),
        ("clean", None, "Clean cache and remove temp files before build"),
        ("strip", "s", "Strip the symbol-table"),
    ]

    boolean_options = ["one-file", "windowed", "clean", "strip"]

    def initialize_options(self):
        self.target = None
        self.pyinstaller_path = None
        self.pyinstaller_opts = None
        self.name = None
        self.one_file = None
        self.icon = None
        self.windowed = None
        self.clean = None
        self.strip = None

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
        if self.one_file:
            self.pyinstaller_opts.append('--one-file')
        if self.strip:
            self.pyinstaller_opts.append('--strip')
        if self.clean:
            self.pyinstaller_opts.append('--clean')
        if self.windowed:
            self.pyinstaller_opts.append('--windowed')
        if self.icon:
            self.pyinstaller_opts.append('--icon=%s' % self.icon)
        self.pyinstaller_opts.append('--name=%s' % self.name)

    def run(self):
        if not self.target:
            raise DistutilsOptionError("no target app is specified to bundle")
        pi = self.pyinstaller_path
        opts = self.pyinstaller_opts + self.target
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
