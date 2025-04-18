import os.path
from unittest import TestCase
from tempfile import TemporaryDirectory

from pywg.lib.wg_log import wg_log, WgLogLevel
from pywg.lib.wg_consts import wg_consts
from pywg.lib.wg_utils import WgWorkDir, WgFileUtils

TEMPLATES_PATH = "./pywg/templates"

class TestWgWorkDir(TestCase):

    def test_get_file_names(self):
        server_name = "test_server"
        client_name = "test_client"
        work_dir = WgWorkDir("/var/pywg")

        self.assertEqual("/var/pywg/data/%s/_server.yaml" % server_name,
                         work_dir.get_server_data_filename(server_name))
        self.assertEqual("/var/pywg/data/%s/%s.yaml" % (server_name, client_name),
                         work_dir.get_client_data_filename(server_name, client_name))

        self.assertEqual("/var/pywg/conf/_servers/%s.conf" % server_name,
                         work_dir.get_server_conf_filename(server_name))
        self.assertEqual("/var/pywg/conf/%s/%s.conf" % (client_name, server_name),
                         work_dir.get_client_conf_filename(server_name, client_name))

class TestWgFileUtils(TestCase):

    def setUp(self):
        self._temp_dir = TemporaryDirectory()
        self._work_dir = WgWorkDir(self._temp_dir.name)
        self._file_utils = WgFileUtils(self._work_dir)

        self._server_name = "test_server"
        self._client_name = "test_client"

        wg_log.set_log_level(WgLogLevel.NONE)

    def tearDown(self):
        self._temp_dir.cleanup()

    def test_file_utils(self):

        # ---------------
        # write/read data
        # ---------------

        # write server data
        self._file_utils.write_server_data({}, self._server_name)

        server_data_file = self._work_dir.get_server_data_filename(self._server_name)
        self.assertTrue(os.path.exists(server_data_file))

        # read server data
        server_data = self._file_utils.read_server_data(self._server_name)
        self.assertEqual(self._server_name, server_data[wg_consts.SERVER_NAME])
        self.assertTrue(wg_consts.PVT_KEY in server_data)
        self.assertTrue(wg_consts.PUB_KEY in server_data)


        # write client data
        # -----------------
        self._file_utils.write_client_data({}, self._server_name, self._client_name)

        client_data_file = self._work_dir.get_client_data_filename(self._server_name, self._client_name)
        self.assertTrue(os.path.exists(client_data_file))


        # read client data
        clients_data = self._file_utils.read_clients_data(self._server_name)
        self.assertEqual(1, len(clients_data))

        client_data = clients_data[0]
        self.assertEqual(self._client_name, client_data[wg_consts.CLIENT_NAME])
        self.assertTrue(wg_consts.PVT_KEY in client_data)
        self.assertTrue(wg_consts.PUB_KEY in client_data)
        self.assertTrue(wg_consts.PSK in client_data)


        # -------------
        # write configs
        # -------------

        # write server config
        self._file_utils._write_server_config(server_data, client_data)

        server_conf_file = self._work_dir.get_server_conf_filename(self._server_name, False)
        self.assertTrue(os.path.exists(server_conf_file))

        # write client config
        self._file_utils._write_clients_config(server_data, clients_data)

        client_conf_file = self._work_dir.get_client_conf_filename(self._server_name, self._client_name, False)
        self.assertTrue(os.path.exists(client_conf_file))
