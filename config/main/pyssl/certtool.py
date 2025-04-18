import os
import jinja2
import subprocess

import yaml

from yaml.loader import SafeLoader
from pathlib import Path

from commons import CommonArgs
from pyssl import TEMPLATES_PATH


def _ssl_gen_pvt_key(filename):
    subprocess.call(["certtool", "--generate-privkey",
                    "--sec-param", "High",
                    "--outfile", filename],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _ssl_gen_self_signed_ca(filenames):
    subprocess.run(["certtool", "--generate-self-signed",
                    "--load-privkey", filenames["pvt_key"],
                    "--template", filenames["template"],
                    "--outfile", filenames["pub_key"]],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _ssl_gen_certificate(ca_filenames, cert_filenames):
    subprocess.call(["certtool", "--generate-certificate",
                    "--load-ca-privkey", ca_filenames["pvt_key"],
                    "--load-ca-certificate", ca_filenames["pub_key"],
                    "--template", cert_filenames["template"],
                    "--load-privkey", cert_filenames["pvt_key"],
                    "--outfile", cert_filenames["pub_key"]],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def _extract_cn_from_crt(filename):
    cmd = "certtool -i < \"%s\" | egrep \"^\\s+Subject: CN=\" | sed -e 's#.*=##'" % filename
    return subprocess.check_output(["bash", "-c", cmd], text=True).strip()


def _create_path(path_name: str):
    if not Path(path_name).exists():
        os.mkdir(path_name)


def _get_or_default(data, name, default):
    if name in data and data[name] is not None:
        return data[name]
    else:
        return default


def _build_dn(data):
    default = "dc=" + data["cn"].replace(".", ",dc=")
    return _get_or_default(data, "dn", default)


class SSLWorkdir:

    def __init__(self, workdir: str, ca_name: str, mkdir: bool = False):
        self._ca_root = os.path.join(workdir, ca_name)
        self._ca_path = os.path.join(self._ca_root, "ca")
        self._cert_path = os.path.join(self._ca_root, "certs")
        self._templates_path = os.path.join(self._ca_root, "templates")
        self._ca_filenames = {
            "template": os.path.join(self._templates_path, "%s.info" % ca_name),
            "pvt_key": os.path.join(self._ca_path, "%s.key" % ca_name),
            "pub_key": os.path.join(self._ca_path, "%s.crt" % ca_name)
        }
        if mkdir:
            self.mkdir()

    def mkdir(self):
        _create_path(self._ca_root)
        _create_path(self._ca_path)
        _create_path(self._cert_path)
        _create_path(self._templates_path)

    def get_ca_filenames(self):
        return self._ca_filenames

    def get_cert_filenames(self, cn):
        return {
            "template": os.path.join(self._templates_path, "%s.info" % cn),
            "pvt_key": os.path.join(self._cert_path, "%s.key" % cn),
            "pub_key": os.path.join(self._cert_path, "%s.crt" % cn)
        }

    def get_ca_pub_key(self, verify: bool = False):
        ca_pub_key = self._ca_filenames["pub_key"]
        if verify and not Path(ca_pub_key).exists():
            raise Exception("CA common name not set and CA certificate does not exist: %s" % ca_pub_key)
        return ca_pub_key


class CertTool:

    def __init__(self, args: CommonArgs):
        self._work_dir = args.get_work_dir()
        self._filename = args.get_config_file()

        loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
        self._jenv = jinja2.Environment(loader=loader, undefined=jinja2.StrictUndefined)

    def generate(self):
        with open(self._filename) as f:
            yaml_data = yaml.load(f, Loader=SafeLoader)
        if "ssl" not in yaml_data:
            raise Exception("File `%s` does not contain `ssl` node" % self._filename)
        ca_list = yaml_data["ssl"]
        for ca_name in ca_list:
            self._process_ca(ca_name, ca_list[ca_name])

    def _process_ca(self, ca_name, ca_data):
        ssl_work_dir = SSLWorkdir(self._work_dir, ca_name, True)

        if "cn" in ca_data:
            self._generate_ca(ca_name, ca_data, ssl_work_dir)
        else:
            ca_data["cn"] = _extract_cn_from_crt(ssl_work_dir.get_ca_pub_key(True))

        for cert in ca_data["certs"]:
            self._generate_cert(ca_data, cert, ssl_work_dir)

    def _generate_ca(self, ca_name, ca_data, ssl_work_dir):
        filenames = ssl_work_dir.get_ca_filenames()

        if Path(filenames["pvt_key"]).exists():
            return

        template = self._jenv.get_template("ca.info.j2")
        f = open(filenames["template"], "w")
        f.write(template.render(data=ca_data))
        f.close()

        _ssl_gen_pvt_key(filenames["pvt_key"])
        _ssl_gen_self_signed_ca(filenames)

        print("** ssl/ca created: " + ca_name)

    def _generate_cert(self, ca_data, cert, ssl_work_dir):
        ca_filenames = ssl_work_dir.get_ca_filenames()
        cert_filenames = ssl_work_dir.get_cert_filenames(cert["cn"])
        if Path(cert_filenames["pvt_key"]).exists():
            return

        template_data = {
            "cn": cert["cn"],
            "dn": _build_dn(cert),
            "organization": _get_or_default(cert, "organization", ca_data["cn"])
        }
        template = self._jenv.get_template("cert.info.j2")
        f = open(cert_filenames["template"], "w")
        f.write(template.render(data=template_data))
        f.close()

        _ssl_gen_pvt_key(cert_filenames["pvt_key"])
        _ssl_gen_certificate(ca_filenames, cert_filenames)

        print("** ssl/cert created: " + cert["cn"])
