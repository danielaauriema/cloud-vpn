import os
import jinja2

import yaml

from yaml.loader import SafeLoader

from commons import CommonArgs
from pynginx import TEMPLATES_PATH

class Nginx:

    def __init__(self, args: CommonArgs):
        self._work_dir = args.get_work_dir()
        self._filename = args.get_config_file()

        loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
        self._jenv = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)

    def generate(self):
        with open(self._filename) as f:
            yaml_data = yaml.load(f, Loader=SafeLoader)

        nginx_data = yaml_data["nginx"]

        for server_name in nginx_data:
            data = nginx_data[server_name]
            self._generate_server_config(server_name, data)

    def _generate_server_config(self, server_name, data):
        template = self._jenv.get_template("%s.conf" % data["template"])
        filename = os.path.join(self._work_dir, "%s.conf" % server_name)

        f = open(filename, "w")
        f.write(template.render(data=data))
        f.close()

        print("** nginx config created: " +server_name)
