import sys
import os
import logging

sys.path.append(
    f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src"
)
import log
import run_parser
import run_findvnet
from spiceutil import Spiceutil


def test_002_parser():
    output_prefix = "tests_result/test_002_parser"
    filename = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/tests_data/test_002_parser.toml"
    args = f"spiceutil.py {output_prefix} {filename}"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_002_parser()
