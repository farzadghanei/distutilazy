"""
distutilazy
-----------

Extra distutils command classes.

:license: MIT, see LICENSE for more details.
"""

from os.path import dirname, abspath
import sys

__version__ = "0.4.0"
__all__ = ("clean", "pyinstaller", "command")

base_dir = abspath(dirname(dirname(__file__)))
if base_dir not in sys.path:
    if len(sys.path):
        sys.path.insert(1, base_dir)
    else:
        sys.path.append(base_dir)
