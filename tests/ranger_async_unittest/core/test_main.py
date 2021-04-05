import optparse
import os
import signal
import sys
from multiprocessing import Process
from test.test_asyncio.test_subprocess import SubprocessThreadedWatcherTests
from unittest.mock import patch  # noqa: WPS458

from support import RangerAsyncTestSupportSignalMixin, RangerAsyncTestSupportStdinMixin, delayed

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


@patch('ranger_async.core.main.sys.stdin', spec=sys.stdin)
@patch(
    'ranger_async.core.main.parse_arguments',
    return_value=optparse.Values(defaults=default_args),
)
class RangerAsyncCoreMainTestsMixin(
    RangerAsyncTestSupportStdinMixin, RangerAsyncTestSupportSignalMixin
):
    def test_main_loop(self, mock_parse, mock_stdin):

        p = Process(
            target=delayed(os.write, delay=0.2), args=(self.win, b':quit\n')  # noqa: WPS432
        )
        p.start()
        res = self.loop.run_until_complete(ra_core_main.main())
        p.join()

        self.assertEqual(res, 0)

    def test_main_cancel(self, mock_parse, mock_stdin):

        for i, debug in enumerate([True, False]):
            with self.subTest(i=i):
                mock_parse.return_value = optparse.Values(
                    defaults={**default_args, **{'debug': debug}}
                )
                p1 = Process(
                    target=delayed(
                        RangerAsyncTestSupportSignalMixin.raise_signal, delay=0.3  # noqa: WPS432
                    ),
                    args=(os.getpid(), signal.SIGINT),
                )
                p2 = Process(target=delayed(os.write, delay=0.5), args=(self.win, b':quit\n'))
                p1.start()
                p2.start()
                res = self.loop.run_until_complete(ra_core_main.main())
                p1.join()
                p2.join()

                from ranger_async import args

                self.assertEqual(args.debug, debug)
                self.assertEqual(res, 0)
                os.set_blocking(self.rin, False)
                if debug:
                    self.assertEqual(os.read(self.rin, 100), b':quit\n')
                else:
                    with self.assertRaises(BlockingIOError):
                        os.read(self.rin, 100)  # noqa: WPS220


class RangerAsyncCoreMainTests(SubprocessThreadedWatcherTests, RangerAsyncCoreMainTestsMixin):
    def setUp(self):
        super().setUp()
        RangerAsyncCoreMainTestsMixin.setUp(self)

    def tearDown(self):
        RangerAsyncCoreMainTestsMixin.tearDown(self)
        super().tearDown()
