#
import sys
import os
import logging

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import log
import run_makeiprobe
import parser
from spiceutil import Spiceutil


def test_makeiprobe_001():
    output_prefix = "test_makeiprobe_001"
    filename = (
        f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc"
    )
    args = f"spiceutil.py {output_prefix} {filename} makeiprobe -net vdd vss vddq vssq -all_probe"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_makeiprobe_001()
