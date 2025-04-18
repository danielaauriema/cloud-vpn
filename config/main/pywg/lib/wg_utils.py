import os
import yaml
import jinja2
import fnmatch
import subprocess

from yaml.loader import SafeLoader

from pywg import TEMPLATES_PATH
from pywg.lib.wg_defaults import wg_defaults
from pywg.lib.wg_log import wg_log
from pywg.lib.wg_consts import wg_consts

def _wg_gen_keys(gen_psk : bool):
  pvt_key = subprocess.run(["wg", "genkey"], stdout=subprocess.PIPE, text=True).stdout.strip()
  result = {
    wg_consts.PVT_KEY: pvt_key,
    wg_consts.PUB_KEY: subprocess.run(["wg", "pubkey"], stdout=subprocess.PIPE, text=True, input=pvt_key).stdout.strip()
  }
  if gen_psk:
    result[wg_consts.PSK] = subprocess.run(["wg", "genpsk"], stdout=subprocess.PIPE, text=True).stdout.strip()
  return result

def _wg_write_config(f, data):
  for key in data:
    if isinstance(data[key], (int, float)):
      f.write("%s: %s\n" % (key, f'{data[key]}'))
    else:
      f.write("%s: \"%s\"\n" % (key, f'{data[key]}'))

def _wg_write_keys(f, gen_psk = False):
  _wg_write_config(f, _wg_gen_keys(gen_psk))


# -----------------
# --- WgWorkDir ---
# -----------------

class WgWorkDir:

  def __init__(self, work_dir):
    self._data_path = os.path.join(work_dir, "data")
    self._conf_path = os.path.join(work_dir, "conf")

  # ------------------
  # data file handlers
  # ------------------

  def get_server_data_path(self, server_name):
    return os.path.join(self._data_path, server_name)

  def get_server_data_filename(self, server_name, create_path = False):
    server_data_path = self.get_server_data_path(server_name)
    if create_path:
      os.makedirs(server_data_path, exist_ok=True)
    return os.path.join(server_data_path, "_server.yaml")

  def get_client_data_filename(self, server_name, client_name):
    server_data_path = self.get_server_data_path(server_name)
    return os.path.join(server_data_path, client_name + ".yaml")

  # --------------------
  # config file handlers
  # --------------------

  def get_server_conf_filename(self, server_name, create_path = False):
    server_conf_path = os.path.join(self._conf_path, "_servers")
    if create_path:
      os.makedirs(server_conf_path, exist_ok=True)
    return os.path.join(server_conf_path, server_name + ".conf")

  def get_client_conf_filename(self, server_name, client_name, create_path = False):
    client_conf_path = os.path.join(self._conf_path, client_name)
    if create_path:
      os.makedirs(client_conf_path, exist_ok=True)
    return os.path.join(client_conf_path, server_name + ".conf")


# -------------------
# --- WgFileUtils ---
# -------------------

class WgFileUtils:

  def __init__(self, work_dir: WgWorkDir):
    self._work_dir = work_dir

    loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
    jenv = jinja2.Environment(loader=loader)
    self._client_template = jenv.get_template("client.conf.j2")
    self._server_template = jenv.get_template("server.conf.j2")

  # ----------------
  # write data files
  # ----------------

  def write_server_data(self, data, server_name):
    filename = self._work_dir.get_server_data_filename(server_name, True)
    if os.path.isfile(filename): return
    data[wg_consts.SERVER_NAME] = server_name

    f = open(filename, "w")
    _wg_write_config(f, data)
    _wg_write_keys(f, False)
    f.close()

    wg_log.info("server config added: " + server_name)

  def write_client_data(self, data, server_name, client_name):
    filename = self._work_dir.get_client_data_filename(server_name, client_name)
    if os.path.isfile(filename): return
    data[wg_consts.CLIENT_NAME] = client_name

    f = open(filename, "w")
    _wg_write_config(f, data)
    _wg_write_keys(f, True)
    f.close()

    wg_log.info("client config added: %s/%s" % (server_name, client_name))

  # ---------------
  # read data files
  # ---------------

  def read_server_data(self, server_name):
    filename = self._work_dir.get_server_data_filename(server_name)
    with open(filename) as f:
      data = yaml.load(f, Loader=SafeLoader)
    wg_defaults.set_server_defaults(data)
    return data

  def read_clients_data(self, server_name):
    clients = []
    data_path = self._work_dir.get_server_data_path(server_name)
    for filename in os.listdir(data_path):
      if not fnmatch.fnmatch(filename, '_*.yaml'):
        client_data_filename = os.path.join(data_path, filename)
        with open(client_data_filename) as f:
          config = yaml.load(f, Loader=SafeLoader)
          wg_defaults.set_client_defaults(config)
          clients.append(config)
    return clients

  # ------------------
  # write config files
  # ------------------

  def build_configs(self, server_name):
    server_config = self.read_server_data(server_name)
    clients_config = self.read_clients_data(server_name)
    self.write_configs(server_config, clients_config)

  def write_configs (self, server, clients):
    self._write_server_config(server, clients)
    self._write_clients_config(server, clients)
    wg_log.info("config created: " + server["server_name"])

  def _write_server_config (self, server, clients):
      filename = self._work_dir.get_server_conf_filename(server["server_name"], True)

      f = open(filename, "w")
      f.write (self._server_template.render(server=server, clients=clients))
      f.close()

  def _write_clients_config (self, server, clients):
    for client in clients:
      filename = self._work_dir.get_client_conf_filename(server["server_name"], client["client_name"], True)
      f = open(filename, "w")
      f.write (self._client_template.render(server=server, client=client))
      f.close()
