import sys
import os
import unittest

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/spiceutil"
)
from spiceutil import Spiceutil


def test_001_args():
    output_prefix = "tests/test_001_args"
    filename = f"dummy.ckt"
    func = f"makeiprobe"
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
    ]
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    test_001_args()
