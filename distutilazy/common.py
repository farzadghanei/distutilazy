# This file is part of distutilazy released under the MIT license.
# See the LICENSE for more information.

import os
import fnmatch

def find_files(root, pattern):
    """Finds all files matching the glob pattern recursively

    :param root: string
    :param pattern: string
    :return list of filepaths relative to root
    """
    results = []
    for base, dirs, files in os.walk(root):
        matched = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in matched)
    return results
