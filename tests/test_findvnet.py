#
import sys
import os
import logging

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import log
import parser
import run_findvnet
import run_findvnet
from spiceutil import Spiceutil


def test_findvnet_001():
    # output_prefix = "test_findvnet_001"
    # filename = (
    #    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc"
    # )
    output_prefix = "test_findvnet_002"
    filename = (
        f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/002.spc"
    )
    args = f"spiceutil.py {output_prefix} {filename} findvnet -net vdd vss vddq vssq"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_findvnet_001()
