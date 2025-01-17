# This plugin adds opened files to `fasd`

from __future__ import (absolute_import, division, print_function)

import subprocess

import ranger_async.api
from ranger_async.ext.spawn import check_output


HOOK_INIT_OLD = ranger_async.api.hook_init


def hook_init(fm):
    def fasd_add():
        for fobj in fm.thistab.get_selection():
            try:
                check_output(['fasd', '--add', fobj.path])
            except subprocess.CalledProcessError:
                pass
    fm.signal_bind('execute.before', fasd_add)
    return HOOK_INIT_OLD(fm)


ranger_async.api.hook_init = hook_init
