import os

from unittest import TestCase
from tempfile import TemporaryDirectory

from commons import CommonArgs
from pydns.bind9 import Bind9

class TestSSLLib(TestCase):

    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self._work_dir = self._temp_dir.name
        self._files_path = os.path.join(
            os.path.dirname(__file__), "files")

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_generate_dns(self):
        args = [self._work_dir, self._get_filename("dns.yaml")]
        ssl_args = CommonArgs("test", args)
        Bind9(ssl_args).generate()

        self.assertTrue(os.path.exists(self._work_dir + "/named.conf"))
        self.assertTrue(os.path.exists(self._work_dir + "/named.conf.options"))
        self.assertTrue(os.path.exists(self._work_dir + "/cloud-vpn.internal"))
        self.assertTrue(os.path.exists(self._work_dir + "/zone2.internal"))

    def _get_filename(self, filename):
        return os.path.join(self._files_path, filename)
