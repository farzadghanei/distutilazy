"""
distutilazy.command
-------------------

Extra distutils commands using command classes provided by distutilazy

:license: MIT, see LICENSE for more details.
"""

from os.path import abspath, dirname
import sys

__all__ = ("clean_pyc", "clean_all", "clean_jython_class",
           "bdist_pyinstaller", "test")

base_dir = abspath(dirname(dirname(dirname(__file__))))
if base_dir not in sys.path:
    if len(sys.path):
        sys.path.insert(1, base_dir)
    else:
        sys.path.append(base_dir)
