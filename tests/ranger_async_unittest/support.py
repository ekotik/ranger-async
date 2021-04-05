import asyncio
import curses
import os
import signal
import sys


def delayed(func, delay=0.1):
    import time

    def delayed_call(*args, **kwargs):
        time.sleep(delay)
        func(*args, **kwargs)

    return delayed_call


class RangerAsyncTestSupportSignalMixin:
    @staticmethod
    def signal_default(sig):
        signal.signal(sig, signal.SIG_DFL)

    @staticmethod
    def raise_signal(pid, sig):
        os.kill(pid, sig)


class RangerAsyncTestSupportStdinMixin:
    def setUp(self):
        os.environ['TERM'] = os.getenv('TERM', default='linux')
        self._stdin = sys.stdin.fileno()
        self.rin, self.win = os.pipe2(os.O_NONBLOCK)  # noqa: WPS414

        os.dup2(self.rin, sys.stdin.fileno())

    def tearDown(self):
        os.dup2(self._stdin, sys.stdin.fileno())

        os.close(self.rin)
        os.close(self.win)


class RangerAsyncTestSupportCursesMixin:
    def setUp(self):
        curses.initscr()

    def tearDown(self):
        curses.endwin()


class RangerAsyncTestSupportAsyncioLoopMixin:
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler = signal.signal
        self.loop.remove_signal_handler = RangerAsyncTestSupportSignalMixin.signal_default

    def tearDown(self):
        pass
