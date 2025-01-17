# This file is part of ranger-async, the console file manager.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from __future__ import absolute_import, division, print_function

from os.path import abspath, dirname, ismount, realpath


def mount_path(path):
    """Get the mount root of a directory"""
    path = abspath(realpath(path))
    while path != "/":
        if ismount(path):
            return path
        path = dirname(path)
    return "/"
