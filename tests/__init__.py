"""
    distutilazy.tests
    -----------------

    Tests for distutilazy

    :license: MIT, see LICENSE for more details.
"""

import os

__all__ = ["test_util", "test_clean"]

for file_ in os.listdir(os.path.dirname(__file__)):
    if file_.startswith('test_') and file_.endswith('.py'):
        __all__.append(file_.rsplit('.py', 1)[0])
