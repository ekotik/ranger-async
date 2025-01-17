# This file is part of ranger-async, the console file manager.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from __future__ import absolute_import, division, print_function

import collections


class OpenStruct(dict):
    """The fusion of dict and struct"""

    def __init__(self, *args, **keywords):
        dict.__init__(self, *args, **keywords)
        self.__dict__ = self


class DefaultOpenStruct(collections.defaultdict):
    """The fusion of dict and struct, with default values"""

    def __init__(self, *args, **keywords):
        collections.defaultdict.__init__(self, None, *args, **keywords)
        self.__dict__ = self

    def __getattr__(self, name):
        if name not in self.__dict__:
            return None
        return self.__dict__[name]
