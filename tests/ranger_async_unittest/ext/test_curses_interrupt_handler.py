import asyncio
import signal
import sys
import unittest

from support import (
    RangerAsyncTestSupportAsyncioLoopMixin,
    RangerAsyncTestSupportCursesMixin,
    RangerAsyncTestSupportSignalMixin,
)

from ranger_async.ext.curses_interrupt_handler import (  # noqa: WPS450
    _interrupt_handler,
    catch_interrupt,
    install_interrupt_handler,
    restore_interrupt_handler,
)


class RangerAsyncExtHandlerTestsMixin(RangerAsyncTestSupportCursesMixin):
    def setUp(self):
        super().setUp()
        signal.signal(signal.SIGINT, lambda: KeyboardInterrupt())  # noqa: WPS506

    def tearDown(self):
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        super().tearDown()

    def test_interrupt(self):
        for i, catch in enumerate([True, False]):
            with self.subTest(i=i):
                catch_interrupt(catch)
                if catch:
                    _interrupt_handler(signal.SIGINT, sys._getframe())  # noqa: WPS437
                else:
                    with self.assertRaises(KeyboardInterrupt):
                        _interrupt_handler(signal.SIGINT, sys._getframe())  # noqa: WPS220,WPS437


class RangerAsyncExtHandlerTests(unittest.TestCase, RangerAsyncExtHandlerTestsMixin):
    def setUp(self):
        RangerAsyncExtHandlerTestsMixin.setUp(self)

    def tearDown(self):
        RangerAsyncExtHandlerTestsMixin.tearDown(self)


class RangerAsyncExtHandlerLoopTestsMixin(
    unittest.TestCase, RangerAsyncTestSupportCursesMixin, RangerAsyncTestSupportAsyncioLoopMixin
):
    def setUp(self):
        RangerAsyncTestSupportCursesMixin.setUp(self)
        RangerAsyncTestSupportAsyncioLoopMixin.setUp(self)

    def tearDown(self):
        RangerAsyncTestSupportCursesMixin.tearDown(self)
        RangerAsyncTestSupportAsyncioLoopMixin.tearDown(self)

    async def yield_signal(self):
        yield
        signal.raise_signal(signal.SIGINT)

    async def consume_signal(self):
        async for i in self.yield_signal():  # noqa: WPS328
            pass

    def test_install_interrupt(self):
        self.loop.call_soon(install_interrupt_handler)
        self.loop.run_until_complete(self.consume_signal())

    def test_restore_interrupt(self):
        self.loop.call_soon(restore_interrupt_handler)
        with self.assertRaises(KeyboardInterrupt):
            self.loop.run_until_complete(self.consume_signal())
