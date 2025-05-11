#
import sys
import os
import logging

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import log
import run_makeiprobe
import run_parser
from spiceutil import Spiceutil


def test_006_flatten():
    output_prefix = "tests_result/test_006_flatten"
    filename = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/tests_data/test_006_flatten.toml"
    args = f"spiceutil.py {output_prefix} {filename}"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_006_flatten()
