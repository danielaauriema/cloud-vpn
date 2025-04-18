import yaml

from yaml.loader import SafeLoader

from commons import CommonArgs
from pywg.lib.wg_utils import WgWorkDir, WgFileUtils

class Wireguard:

    def __init__(self, args: CommonArgs):
        self._work_dir = args.get_work_dir()
        self._config_file = args.get_config_file()

        work_dir = WgWorkDir(self._work_dir)
        self._file_utils = WgFileUtils(work_dir)

    def generate(self):
        with open(self._config_file) as f:
            yaml_data = yaml.load(f, Loader=SafeLoader)
        servers = yaml_data["wireguard"]
        for server_name in servers:
            self._load_server(server_name, servers[server_name])
            self._file_utils.build_configs(server_name)

    def _load_server(self, server_name, data):
        server_data = data["server"]
        self._file_utils.write_server_data(server_data, server_name)
        self._load_clients(data["clients"], server_name)

    def _load_clients(self, data, server_name):
        if isinstance(data, dict):
            for client_name in data:
                self._file_utils.write_client_data(data[client_name], server_name, client_name)
        else:
            for client_name in data:
                self._file_utils.write_client_data({}, server_name, client_name)


