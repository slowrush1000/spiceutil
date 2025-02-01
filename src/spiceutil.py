#
import sys
import datetime
import logging
import log
import makeiprobe
import netlist
import parser


class Spiceutil:
    def __init__(self):
        self.m_output_prefix = ""
        self.m_log = None

    def set_output_prefix(self, output_prefix):
        self.m_output_prefix = output_prefix

    def get_output_prefix(self):
        return self.m_output_prefix

    def set_log(self, log):
        self.m_log = log

    def get_log(self):
        return self.m_log

    def print_usage(self):
        print(f"{netlist.get_program()} {netlist.get_version()}")
        print(f"spiceutil.py usage:")
        print(
            f"spiceutil.py output_prefix makeiprobe filename [-net NET [NET ...]] [-top_cell TOP_CELL] [-all_probe] [-debug]"
        )
        print(f"spiceutil.py output_prefix flatten filename [-top_cell TOP_CELL]")
        print(f"spiceutil.py output_prefix findvnet filename [-net NET [NET ...]]")
        print(
            f"spiceutil.py output_prefix findcellcap filename [-power_net POWER_NET] [-ground_net GROUND_NET]"
        )

    def init_log(self, output_prefix):
        self.set_output_prefix(output_prefix)
        my_log = log.Log(output_prefix)
        self.set_log(my_log)

    def run(self, args):
        if 5 > len(args):
            self.print_usage()
            exit()
        self.init_log(args[1])
        print(f"args: {args}")
        #
        self.get_log().get_logger().info(
            f"# spiceutil.py start ... {datetime.datetime.now()}"
        )
        #
        # self.get_log().get_logger().info(f"debug- {args[2]}")
        if "makeiprobe" == args[2].lower():
            # self.get_log().get_logger().info(f"debug- makeiprbe")
            my_makeiprobe = makeiprobe.Makeiprobe(self.get_log())
            my_makeiprobe.run(args[1:])
        #
        self.get_log().get_logger().info(
            f"# spiceutil.py end ... {datetime.datetime.now()}"
        )


def main(args):
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    main(sys.argv)
