from unittest import TestCase

from pywg.lib.wg_log import WgLog, WgLogLevel

from io import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class TestWgLog(TestCase):

    def setUp(self):
        self._args = ["/var/pywg",  "test_server"]

    def test_get_log_level__info(self):
        self.assertEqual(WgLogLevel.INFO, WgLogLevel.get_log_level({}))
        self.assertEqual(WgLogLevel.INFO, WgLogLevel.get_log_level({"debug": False}))
        self.assertEqual(WgLogLevel.INFO, WgLogLevel.get_log_level({"log_level": "info"}))

    def test_get_log_level__debug(self):
        self.assertEqual(WgLogLevel.DEBUG, WgLogLevel.get_log_level({"debug": True}))
        self.assertEqual(WgLogLevel.DEBUG, WgLogLevel.get_log_level({"log_level": "debug"}))

    def test_get_log_level__none(self):
        self.assertEqual(WgLogLevel.NONE, WgLogLevel.get_log_level({"log_level": "none"}))

    def test_wg_log__info(self):
        log = WgLog(WgLogLevel.INFO)
        with Capturing() as output_info:
            log.info("test message")
        with Capturing() as output_debug:
            log.debug("test message")
        self.assertEqual(["[INFO ] test message"], output_info)
        self.assertEqual([], output_debug)

    def test_wg_log__debug(self):
        log = WgLog(WgLogLevel.DEBUG)
        with Capturing() as output_info:
            log.info("test message")
        with Capturing() as output_debug:
            log.debug("test message")
        self.assertEqual(["[INFO ] test message"], output_info)
        self.assertEqual(["[DEBUG] test message"], output_debug)

    def test_wg_log__none(self):
        log = WgLog(WgLogLevel.NONE)
        with Capturing() as output_info:
            log.info("test message")
        with Capturing() as output_debug:
            log.debug("test message")
        self.assertEqual([], output_info)
        self.assertEqual([], output_debug)
