

from commons import CommonArgs
from pywg.wireguard import Wireguard

if __name__ == "__main__":
    args = CommonArgs("Wireguard config module")
    Wireguard(args).generate()


