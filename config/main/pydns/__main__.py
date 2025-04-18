from commons import CommonArgs
from pydns.bind9 import Bind9

if __name__ == "__main__":
    args = CommonArgs("DNS/Bind9 config module")
    Bind9(args).generate()
