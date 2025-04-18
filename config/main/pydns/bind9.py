import os
import yaml
import jinja2

from yaml.loader import SafeLoader

from commons import CommonArgs
from pydns import TEMPLATES_PATH

def _load_from_file(filename):
    with open(filename) as f:
        config = yaml.load(f, Loader=SafeLoader)["dns"]
    if not "zones" in config:
        config["zones"] = []

    for zone in config["zones"]:
        if not "path" in zone:
            zone["path"] = "."
        if not "subdomains" in zone:
            zone["subdomains"] = []
    return config

class Bind9:

    def __init__(self, args: CommonArgs):
        self._work_dir = args.get_work_dir()
        self._filename = args.get_config_file()

        loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
        self._jenv = jinja2.Environment(loader=loader,undefined=jinja2.StrictUndefined)

    def generate(self):
        source = self._filename
        config = _load_from_file(source)
        zones = config["zones"]

        self._render("named.conf.options", config)
        self._add_zones(zones)
        for zone in zones:
            self._render("domain_data_file", zone, zone["ns_domain"])
            print("** DNS/bind9 config created: " + zone["ns_domain"])

    def _render(self, template, config, output = None):
        _template = self._jenv.get_template("%s.j2" % template)
        _output = template if output is None else output
        filename = os.path.join(self._work_dir, _output)

        f = open(filename, "w")
        f.write(_template.render(config=config))
        f.close()

    def _add_zones(self, zones):

        template = self._jenv.get_template("named.conf.j2")
        filename = os.path.join(self._work_dir, "named.conf")

        f = open(filename, "w")
        f.write(template.render(config=zones))
        f.close()
