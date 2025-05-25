import sys
import os
import unittest

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/spiceutil")
from spiceutil import Spiceutil


def test_001_args():
    output_prefix = "tests/test_001_args"
    func = f"args"
    filename = f"dummy.ckt"
    args = [
        output_prefix,
        func,
        filename,
        "-topcell",
        "test_top_cell",
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
        "-case",
    ]
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    test_001_args()
