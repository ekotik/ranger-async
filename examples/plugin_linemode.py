# Compatible since ranger-async 1.7.0
#
# This sample plugin adds a new linemode displaying the filename in rot13.
# Load this plugin by copying it to ~/.config/ranger-async/plugins/ and activate
# the linemode by typing ":linemode rot13" in ranger-async.  Type Mf to restore
# the default linemode.

from __future__ import (absolute_import, division, print_function)

import codecs

import ranger_async.api
from ranger_async.core.linemode import LinemodeBase


@ranger_async.api.register_linemode
class MyLinemode(LinemodeBase):
    name = "rot13"

    def filetitle(self, fobj, metadata):
        return codecs.encode(fobj.relative_path, "rot_13")

    def infostring(self, fobj, metadata):
        raise NotImplementedError
