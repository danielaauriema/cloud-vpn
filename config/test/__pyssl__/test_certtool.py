import os

from unittest import TestCase
from tempfile import TemporaryDirectory

from commons import CommonArgs
from pyssl.certtool import  CertTool

class TestSSLLib(TestCase):

    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self._work_dir = self._temp_dir.name
        self._files_path = os.path.join(
            os.path.dirname(__file__), "files")

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_generate_ca(self):
        args = [self._work_dir, self._get_filename("test-ca.yaml")]
        ssl_args = CommonArgs("test", args)
        CertTool(ssl_args).generate()

        self.assertTrue(os.path.exists(self._work_dir + "/test-ca"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-ca/ca/test-ca.key"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-ca/templates/test-ca.info"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-ca/ca/test-ca.crt"))

    def test_generate_cert(self):
        args = [self._work_dir, self._get_filename("test-cert.yaml")]
        ssl_args = CommonArgs("test", args)
        CertTool(ssl_args).generate()

        self.assertTrue(os.path.exists(self._work_dir + "/test-cert-ca"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-cert-ca/ca/test-cert-ca.crt"))

        self.assertTrue(os.path.exists(self._work_dir + "/test-cert-ca/certs/test-cert.internal.key"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-cert-ca/templates/test-cert.internal.info"))
        self.assertTrue(os.path.exists(self._work_dir + "/test-cert-ca/certs/test-cert.internal.crt"))

    def test_generate_multi(self):
        args = [self._work_dir, self._get_filename("test-multi.yaml")]
        ssl_args = CommonArgs("test", args)
        CertTool(ssl_args).generate()

        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca1"))
        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca1/certs/multi-ca1.internal.crt"))
        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca1/certs/subdomain.multi-ca1.internal.crt"))

        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca2"))
        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca2/certs/multi-ca2.internal.crt"))
        self.assertTrue(os.path.exists(self._work_dir + "/multi-ca2/certs/subdomain.multi-ca2.internal.crt"))

    def _get_filename(self, filename):
        return os.path.join(self._files_path, filename)
