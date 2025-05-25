import sys
import os

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/spiceutil")
from spiceutil import Spiceutil


def test_002_parser():
    output_prefix = "tests/test_003_makeiprobe"
    filename = "data/001.spc"
    func = "makeiprobe"
    args = [
        output_prefix,
        func,
        filename,
        "-nets",
        "vdd",
        "vss",
        "vddq",
        "vssq",
        "-power_nets",
        "vdd",
        "vddq",
        "-ground_nets",
        "vss",
        "vssq",
        "-debug",
    ]
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    test_002_parser()
