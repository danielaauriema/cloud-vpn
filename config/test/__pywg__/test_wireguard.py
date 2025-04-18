import unittest
from unittest import TestCase
from unittest.mock import MagicMock

import os
from tempfile import TemporaryDirectory

from pywg.lib.wg_utils import WgWorkDir
from pywg.wireguard import Wireguard

from commons import CommonArgs

class TestWgYaml(TestCase):

    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self._work_dir = self._temp_dir.name
        self._wg_work_dir = WgWorkDir(self._work_dir)
        self._files_path = os.path.join(
            os.path.dirname(__file__), "files")

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_load_yaml_from_file(self):
        input_args = ["unittest", self._work_dir,
                      os.path.join( self._files_path, "servers.yaml")]

        with unittest.mock.patch('sys.argv', input_args):
            args = CommonArgs("test")
            Wireguard(args).generate()

        files = self._get_files("server_92", ["client_x92_1", "client_x92_2"])
        files += self._get_files("server_93", ["c93_a", "c93_b"])
        for file in files:
            self.assertTrue(os.path.exists(file), "File does not exist: %s" % file)

    def _get_files(self, server_name, clients):
        files = [
            self._wg_work_dir.get_server_data_filename(server_name),
            self._wg_work_dir.get_server_conf_filename(server_name, server_name)
        ]
        for client_name in clients:
            files += [
                self._wg_work_dir.get_client_data_filename(server_name, client_name),
                self._wg_work_dir.get_client_conf_filename(server_name, client_name)
            ]
        return files