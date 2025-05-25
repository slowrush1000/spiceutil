import sys
import os

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/spiceutil")
from spiceutil import Spiceutil


def test_004_findvnet():
    output_prefix = "tests/test_004_findvnet"
    filename = "data/001.spc"
    func = "findvnet"
    args = [
        output_prefix,
        func,
        filename,
        "-nets",
        "vdd",
        "vss",
        "vddq",
        "vssq",
        "-debug",
    ]
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    test_004_findvnet()
