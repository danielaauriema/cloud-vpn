import copy
from unittest import TestCase

from pywg.lib.wg_consts import wg_consts
from pywg.lib.wg_defaults import WgDefaults

class TestWgDefaults(TestCase):

    def setUp(self):
        self._server_name = "test_server_name"
        self._client_name = "test_client_name"

    def test_set_default_values(self):
        consts = wg_consts
        defaults = WgDefaults()

        server = {
            consts.SERVER_NAME: self._server_name
        }
        defaults.set_server_defaults(server)

        self.assertEqual(7, len(server))
        self.assertEqual(server[consts.SERVER_NAME], self._server_name)
        self.assertEqual(server[consts.LISTEN_PORT], defaults.LISTEN_PORT)
        self.assertEqual(server[consts.ENDPOINT], defaults.ENDPOINT)
        self.assertEqual(server[consts.NETWORK_MASK], defaults.NETWORK_MASK)
        self.assertEqual(server[consts.CLIENT_ALLOWED_IPS], defaults.NETWORK_MASK)
        self.assertEqual(server[consts.PERSISTENT_KEEPALIVE], defaults.PERSISTENT_KEEPALIVE)
        self.assertEqual(server[consts.SERVER_ADDRESS], "172.16.20.1")

        client1 = {
            consts.CLIENT_NAME: self._client_name
        }
        defaults.set_client_defaults(client1)
        self.assertEqual(5, len(client1))
        self.assertEqual(client1[consts.CLIENT_NAME], self._client_name)
        self.assertEqual(client1[consts.CLIENT_ADDRESS], "172.16.20.2")
        self.assertFalse(consts.DNS_SERVERS in client1)
        self.assertEqual(client1[consts.PERSISTENT_KEEPALIVE], defaults.PERSISTENT_KEEPALIVE)
        self.assertEqual(client1[consts.CLIENT_ALLOWED_IPS], server[consts.CLIENT_ALLOWED_IPS])
        self.assertEqual(client1[consts.SERVER_ALLOWED_IPS], client1[consts.CLIENT_ADDRESS] + "/32")

        client2 = {
            consts.CLIENT_NAME: "client2"
        }
        defaults.set_client_defaults(client2)
        self.assertEqual(client2[consts.CLIENT_ADDRESS], "172.16.20.3")

    def test_set_custom_values(self):
        consts = wg_consts
        defaults = WgDefaults()

        server = {
            consts.SERVER_NAME: self._server_name,
            consts.LISTEN_PORT: 12345,
            consts.ENDPOINT: "custom_endpoint",
            consts.NETWORK_MASK: "10.23.0.0/16",
            consts.DNS_SERVERS: "8.8.8.8,8.8.4.4",
            consts.CLIENT_ALLOWED_IPS: "172.16.0.0/16,10.0.0.0/8",
            consts.PERSISTENT_KEEPALIVE: 99,
            consts.SERVER_ADDRESS: "10.23.0.99"
        }
        server_copy = copy.deepcopy(server)

        defaults.set_server_defaults(server)

        self.assertEqual(8, len(server))
        self.assertEqual(server[consts.SERVER_NAME], self._server_name)
        self.assertEqual(server[consts.LISTEN_PORT], server_copy[consts.LISTEN_PORT])
        self.assertEqual(server[consts.ENDPOINT], server_copy[consts.ENDPOINT])
        self.assertEqual(server[consts.NETWORK_MASK], server_copy[consts.NETWORK_MASK])
        self.assertEqual(server[consts.DNS_SERVERS], server_copy[consts.DNS_SERVERS])
        self.assertEqual(server[consts.CLIENT_ALLOWED_IPS], server_copy[consts.CLIENT_ALLOWED_IPS])
        self.assertEqual(server[consts.PERSISTENT_KEEPALIVE], server_copy[consts.PERSISTENT_KEEPALIVE])
        self.assertEqual(server[consts.SERVER_ADDRESS], server_copy[consts.SERVER_ADDRESS])

        client1 = {
            consts.CLIENT_NAME: self._client_name
        }
        defaults.set_client_defaults(client1)
        self.assertEqual(6, len(client1))
        self.assertEqual(client1[consts.CLIENT_NAME], self._client_name)
        self.assertEqual(client1[consts.CLIENT_ADDRESS], "10.23.0.2")
        self.assertEqual(client1[consts.DNS_SERVERS], server_copy[consts.DNS_SERVERS])
        self.assertEqual(client1[consts.PERSISTENT_KEEPALIVE], server_copy[consts.PERSISTENT_KEEPALIVE])
        self.assertEqual(client1[consts.CLIENT_ALLOWED_IPS], server_copy[consts.CLIENT_ALLOWED_IPS])
        self.assertEqual(client1[consts.SERVER_ALLOWED_IPS], client1[consts.CLIENT_ADDRESS] + "/32")

        client2 = {
            consts.CLIENT_NAME: "client2",
            consts.CLIENT_ADDRESS: "10.23.1.99",
            consts.DNS_SERVERS: "10.23.0.10",
            consts.PERSISTENT_KEEPALIVE: 123,
            consts.CLIENT_ALLOWED_IPS: "10.23.0.0/24,10.23.1.0/24",
            consts.SERVER_ALLOWED_IPS: "10.23.1.99/32,10.23.2.0/24"
        }
        client2_copy = copy.deepcopy(client2)
        defaults.set_client_defaults(client2)
        self.assertEqual(6, len(client2))
        self.assertEqual(client2[consts.CLIENT_NAME], "client2")
        self.assertEqual(client2[consts.CLIENT_ADDRESS], client2_copy[consts.CLIENT_ADDRESS])
        self.assertEqual(client2[consts.DNS_SERVERS], client2_copy[consts.DNS_SERVERS])
        self.assertEqual(client2[consts.PERSISTENT_KEEPALIVE], client2_copy[consts.PERSISTENT_KEEPALIVE])
        self.assertEqual(client2[consts.CLIENT_ALLOWED_IPS], client2_copy[consts.CLIENT_ALLOWED_IPS])
        self.assertEqual(client2[consts.SERVER_ALLOWED_IPS], client2_copy[consts.SERVER_ALLOWED_IPS])
