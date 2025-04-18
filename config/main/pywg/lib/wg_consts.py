
class WgConsts:

  def __init__(self):
    self.SERVER_NAME = "server_name"
    self.CLIENT_NAME = "client_name"
    self.LISTEN_PORT = "listen_port"
    self.ENDPOINT = "endpoint"
    self.NETWORK_MASK = "network_mask"
    self.ALLOWED_IPS = "allowed_ips"

    self.SERVER_ALLOWED_IPS = "server_allowed_ips"
    self.CLIENT_ALLOWED_IPS = "client_allowed_ips"

    self.PERSISTENT_KEEPALIVE = "persistent_keepalive"
    self.SERVER_ADDRESS = "server_address"
    self.CLIENT_ADDRESS = "client_address"
    self.DNS_SERVERS = "dns_servers"
    self.CLIENT_INDEX = "client_index"

    self.PVT_KEY = "pvt_key"
    self.PUB_KEY = "pub_key"
    self.PSK = "psk"

wg_consts = WgConsts()
