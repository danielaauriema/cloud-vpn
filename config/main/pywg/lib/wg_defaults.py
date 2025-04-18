from netaddr import IPNetwork
from pywg.lib.wg_consts import wg_consts

def _set_if_absent(data, name, value):
  if not name in data:
    data[name] = value

def _set_if_absent_from_data(data, target, source):
  _set_if_absent(data, target, data[source])

class WgNetwork:

  def __init__(self, network_addr: str):
    self._network = IPNetwork(network_addr)
    self._addresses = list(self._network)

  def get_ip(self, index: int):
    return f'{self._addresses[index]}'

class WgDefaults:

  def __init__(self):
    self._index = 2
    self._network = None
    self._server_config = None

    self.LISTEN_PORT = 51820
    self.ENDPOINT = "localhost"
    self.NETWORK_MASK = "172.16.20.0/24"
    self.PERSISTENT_KEEPALIVE = 25

  def set_server_defaults(self, data):
    self._index = 2
    _set_if_absent(data, wg_consts.LISTEN_PORT, self.LISTEN_PORT)
    _set_if_absent(data, wg_consts.ENDPOINT, self.ENDPOINT)
    _set_if_absent(data, wg_consts.NETWORK_MASK, self.NETWORK_MASK)
    _set_if_absent_from_data(data, wg_consts.CLIENT_ALLOWED_IPS, wg_consts.NETWORK_MASK)
    _set_if_absent(data, wg_consts.PERSISTENT_KEEPALIVE, self.PERSISTENT_KEEPALIVE)
    self._network = WgNetwork(data[wg_consts.NETWORK_MASK])
    _set_if_absent(data, wg_consts.SERVER_ADDRESS, self._network.get_ip(1))
    self._server_config = data

  def set_client_defaults(self, data):
    if not wg_consts.CLIENT_ADDRESS in data:
      index = self._get_client_index(data)
      data[wg_consts.CLIENT_ADDRESS] = format(self._network.get_ip(index))
    self._can_replace_by_server_config(data, wg_consts.DNS_SERVERS)
    self._can_replace_by_server_config(data, wg_consts.PERSISTENT_KEEPALIVE)
    _set_if_absent(data, wg_consts.CLIENT_ALLOWED_IPS, self._get_server_config(wg_consts.CLIENT_ALLOWED_IPS))
    _set_if_absent(data, wg_consts.SERVER_ALLOWED_IPS, data[wg_consts.CLIENT_ADDRESS] + "/32")

  # ---------------
  # private methods
  # ---------------

  def _get_client_index(self, data):
    if not wg_consts.CLIENT_INDEX in data:
      self._index += 1
      return self._index - 1
    return data[wg_consts.CLIENT_INDEX]

  def _can_replace_by_server_config(self, data, property_name: str):
    if not property_name in data and property_name in self._server_config:
      data[property_name] = self._get_server_config(property_name)

  def _get_server_config(self, property_name: str):
    return self._server_config[property_name]

wg_defaults = WgDefaults()
