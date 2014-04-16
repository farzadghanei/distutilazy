"""
distutility.command.clean_pyc

command to clean compile python files
"""

import os
import sys

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if not base_dir in sys.path:
    if len(sys.path):
        sys.path.insert(1, base_dir)
    else:
        sys.path.append(base_dir)

import distutilazy.clean

class clean_pyc(distutilazy.clean.clean_pyc):
    pass
