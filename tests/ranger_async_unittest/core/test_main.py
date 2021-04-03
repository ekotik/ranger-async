import asyncio
import curses
import io
import optparse
import os
import sys
from asyncio.unix_events import ThreadedChildWatcher
from test.test_asyncio import utils as test_utils
from test.test_asyncio.test_subprocess import PROGRAM_CAT, SubprocessWatcherMixin
from unittest import mock
from unittest.mock import patch  # noqa: WPS458

from ranger_async.core import main as ra_core_main

default_args = {
    'cachedir': os.path.join(os.getcwd(), 'data/cachedir'),
    'choosedir': os.path.join(os.getcwd(), 'data/choosedir'),
    'clean': None,
    'cmd': None,
    'confdir': os.path.join(os.getcwd(), 'data/confdir'),
    'copy_config': None,
    'datadir': os.path.join(os.getcwd(), 'data/datadir'),
    'debug': None,
    'list_tagged_files': None,
    'list_unused_keys': None,
    'logfile': None,
    'paths': [],
    'profile': None,
    'selectfile': None,
    'show_only_dirs': False,
}


class RangerAsyncTests(SubprocessWatcherMixin, test_utils.TestCase):

    Watcher = ThreadedChildWatcher  # noqa: WPS115

    def setUp(self):
        super().setUp()

        os.environ['TERM'] = 'xterm'
        self._stdin = sys.stdin.fileno()
        self._stdout = sys.stdout.fileno()
        self.rin, self.win = os.pipe()  # noqa: WPS414
        self.rout, self.wout = os.pipe()  # noqa: WPS414

        os.dup2(self.rin, sys.stdin.fileno())
        os.dup2(self.wout, sys.stdout.fileno())

    def tearDown(self):
        super().tearDown()

        os.dup2(self._stdin, sys.stdin.fileno())
        os.dup2(self._stdout, sys.stdout.fileno())

        os.close(self.rin)
        os.close(self.win)
        os.close(self.rout)
        os.close(self.wout)
        os.unsetenv('TERM')

    @patch(
        'ranger_async.core.main.parse_arguments',
        return_value=optparse.Values(defaults=default_args),
    )
    @patch('ranger_async.core.main.sys.stdin')
    def test_main(self, mock_stdin, mock_parse):
        mock_stdin_args = {'isatty.return_value': True}
        mock_stdin.configure_mock(**mock_stdin_args)

        async def run(data_in):
            r, w = os.pipe2(os.O_NONBLOCK | os.O_CLOEXEC)  # noqa: WPS111
            proc = await asyncio.create_subprocess_exec(
                *PROGRAM_CAT,
                stdin=r,
                stdout=self.win,
                stderr=self.win,
            )
            os.write(w, data_in)
            task = asyncio.create_task(proc.communicate(data_in))
            task.add_done_callback(lambda h: map(os.close, [r, w]))
            await proc.communicate()
            res = await asyncio.wait_for(ra_core_main.main(), 1.0)
            return res, proc.returncode

        res, ret = self.loop.run_until_complete(run(b':quit\n'))
        self.assertEqual(res, 0)
        self.assertEqual(ret, 0)
