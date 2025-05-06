#
import sys
import os

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
from spiceutil import Spiceutil


def test_003_findvnet():
    output_prefix = "tests/test_003_findvnet"
    filename = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/tests/test_003_findvnet.toml"
    args = f"spiceutil.py {output_prefix} {filename}"
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args.split())


if __name__ == "__main__":
    test_003_findvnet()
