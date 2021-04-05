import os
import sys
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


def suite_tests(start_dir, pattern="test_*"):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    tests = loader.discover(start_dir=start_dir, pattern=pattern)
    suite.addTests(tests)
    return suite


if __name__ == '__main__':
    tests_dir = os.path.abspath(os.path.dirname(__file__))
    top_dir = os.path.abspath(os.path.dirname(os.path.dirname(tests_dir)))  # noqa: WPS221
    sys.path.append(top_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite_tests(os.path.join(tests_dir, "core")))
    runner.run(suite_tests(os.path.join(tests_dir, "ext")))
