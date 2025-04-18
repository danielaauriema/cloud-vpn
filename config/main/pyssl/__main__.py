from commons import CommonArgs
from pyssl.certtool import CertTool

if __name__ == "__main__":
    args = CommonArgs("SSL config module")
    CertTool(args).generate()
