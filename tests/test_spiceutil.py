import sys
import os
import logging

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import log
import makeiprobe
import parser
from spiceutil import Spiceutil


def test_spiceutil_001():
    output_prefix = "test_spiceutil_001"
    filename = (
        f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc"
    )
    args = f"spiceutil.py {output_prefix}"
    # args = f"spiceutil.py {output_prefix} makeiprobe {filename} -net vdd vss vddq vssq"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_spiceutil_001()
