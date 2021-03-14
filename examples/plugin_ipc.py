# Tested with ranger-async 1.7.0 through ranger-async 1.7.*
#
# This plugin creates a FIFO in /tmp/ranger-async-ipc.<PID> to which any
# other program may write. Lines written to this file are evaluated by
# ranger-async as the ranger-async :commands.
#
# Example:
#   $ echo tab_new ~/images > /tmp/ranger-async-ipc.1234

from __future__ import (absolute_import, division, print_function)

import ranger_async.api


HOOK_INIT_OLD = ranger_async.api.hook_init


def hook_init(fm):
    try:
        # Create a FIFO.
        import os
        ipc_fifo = "/tmp/ranger-async-ipc." + str(os.getpid())
        os.mkfifo(ipc_fifo)

        # Start the reader thread.
        try:
            import thread
        except ImportError:
            import _thread as thread

        def ipc_reader(filepath):
            while True:
                with open(filepath, 'r') as fifo:
                    line = fifo.read()
                    fm.execute_console(line.strip())
        thread.start_new_thread(ipc_reader, (ipc_fifo,))

        # Remove the FIFO on ranger-async exit.
        def ipc_cleanup(filepath):
            try:
                os.unlink(filepath)
            except IOError:
                pass
        import atexit
        atexit.register(ipc_cleanup, ipc_fifo)
    except IOError:
        # IPC support disabled
        pass
    finally:
        HOOK_INIT_OLD(fm)


ranger_async.api.hook_init = hook_init
