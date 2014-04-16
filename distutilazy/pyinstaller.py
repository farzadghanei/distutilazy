"""
distutility.pyinstaller

helper commands for using pyinstaller
"""

version = '0.1.3'

import os
import platform
import subprocess
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
        ("icon=", "i", "Path to icon resource"),
        ("windowed", "w", "Windowed app, no console for stdio"),
        ("clean", None, "Clean cached and temp files before build"),
    ]

    boolean_options = ["windowed", "clean"]

    def initialize_options(self):
        self.target = None
        self.pyinstaller_path = None
        self.pyinstaller_opts = []
        self.name = None
        self.icon = None
        self.windowed = None
        self.clean = None

    def default_pyinstaller_opts(self):
        """Return default options for PyInstaller.
        Use this method to customize the command for separate projects

        :return: list of options
        """
        return ['--onefile']

    def finalize_options(self):
        if self.pyinstaller_path:
            self.pyinstaller_path = os.path.abspath(self.pyinstaller_path)
            if not os.path.exists(self.pyinstaller_path):
                raise DistutilsOptionError("failed to find pyinstaller from %s" % self.pyinstaller_path)
        self.pyinstaller_opts = self.default_pyinstaller_opts()
        if not self.name:
            self.name = self.distribution.metadata.get_name()
        if self.clean:
            self.pyinstaller_opts.append('--clean')
        if self.windowed:
            self.pyinstaller_opts.append('--windowed')
        if self.icon:
            self.pyinstaller_opts.append("--icon=%s" % self.icon)
        if platform.system().upper() != 'WINDWOWS':
            self.pyinstaller_opts.append('--strip')
        self.pyinstaller_opts.append("--name=%s" % self.name)

    def run(self):
        if not self.target:
            raise DistutilsOptionError("no target app is specified to bundle")
        pi = self.pyinstaller_path or 'pyinstaller'
        args = self.pyinstaller_opts
        args.append(self.target)
        args.insert(0, pi)
        self.announce("running %s" % ' '.join(args))
        code = subprocess.call(args)
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
