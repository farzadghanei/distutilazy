"""
distutilazy.command.pyinstaller
-------------------------------

Command to call pyinstaller

:license: MIT, see LICENSE for more details.
"""

from os.path import abspath, dirname
import sys

base_dir = abspath(dirname(dirname(dirname(__file__))))
if base_dir not in sys.path:
    if len(sys.path):
        sys.path.insert(1, base_dir)
    else:
        sys.path.append(base_dir)

import distutilazy.pyinstaller


class bdist_pyinstaller(distutilazy.pyinstaller.BdistPyInstaller):
    pass
