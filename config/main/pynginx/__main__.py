from commons import CommonArgs
from pynginx.nginx import Nginx

if __name__ == "__main__":
    args = CommonArgs("Nginx config module")
    Nginx(args).generate()
