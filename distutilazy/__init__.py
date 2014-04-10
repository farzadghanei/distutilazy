"""
distutilazy

Extra distutil command classes
"""

import os
import sys

version = '0.0.2'
all = ['clean', 'command']

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if not base_dir in sys.path:
    if len(sys.path):
        sys.path.insert(1, base_dir)
    else:
        sys.path.append(base_dir)
