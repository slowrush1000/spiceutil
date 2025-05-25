import argparse
import datetime
import os
import sys

from input import Input
from log import Log
from makeiprobe import Makeiprobe
from findvnet import Findvnet
from netlist import Netlist
from netlist import Parser
from performance import Performance
from utils import Utils
from version import Version


class Spiceutil:
    def __init__(self):
        self.__input = Input()
        self.__netlist = Netlist()
        self.__log = None
        #
        self.__argparser = None
        self.__performance = Performance()

    def get_input(self):
        return self.__input

    def get_netlist(self):
        return self.__netlist

    def get_log(self):
        return self.__log

    def get_performance(self):
        return self.__performance

    def print_usage(self):
        self.__argparser.print_help()

    def init_argparser(self):
        description = (
            f"spiceutil({Version().get_version()})"
            "\n"
            "spice netlist utility\n"
            "\n"
            "example syntax)\n"
            "spiceutil output_prefix args       netlist_file < -topcell topcell >\n"
            "spiceutil output_prefix parser     netlist_file < -topcell topcell > < -case > < -debug >\n"
            "spiceutil output_prefix makeiprobe netlist_file < -topcell topcell > < -nets netname1 ...> < -case > < -all_probe >\n"
            "spiceutil output_prefix findvnet   netlist_file < -topcell topcell > < -nets netname1 ...> < -case >\n"
            "spiceutil output_prefix flatten    netlist_file < -topcell topcell >\n"
            "spiceutil output_prefix finddecap  netlist_file < -topcell topcell > < -power_nets netname1 ... > < -ground_nets netname1 ... > < -case >\n"
        )
        self.__argparser = argparse.ArgumentParser(
            prog=f"{Version().get_program()}",
            formatter_class=argparse.RawTextHelpFormatter,
            description=description,
        )
        #
        self.__argparser.add_argument(
            "output_prefix", type=str, help="output prefix, ex) ${output_prefix}.log"
        )
        self.__argparser.add_argument(
            "func",
            type=str,
            help="func, ex) makeiprobe, findvent, flatten, finddecap",
            choices=["args", "parser", "makeiprobe", "findvnet", "flatten", "finddecap"],
        )
        self.__argparser.add_argument("netlist_file", type=str, help="spice file")
        #
        self.__argparser.add_argument("-topcell", type=str, nargs=1, help="top cell name")
        self.__argparser.add_argument("-nets", type=str, nargs="*", help="netnames")
        self.__argparser.add_argument("-power_nets", type=str, nargs="*", help="power netnames")
        self.__argparser.add_argument("-ground_nets", type=str, nargs="*", help="ground netnames")
        self.__argparser.add_argument(
            "-debug",
            action="store_true",
            help="enable to print debugging information",
        )
        self.__argparser.add_argument(
            "-case", action="store_true", help="enable to case sensitive"
        )
        self.__argparser.add_argument(
            "-dollar_comment", action="store_true", help="enable to dollar($) comments"
        )
        self.__argparser.add_argument(
            "-all_probe", action="store_true", help="enable to all probe(makeprobe)"
        )

    def read_args(self, args):
        self.get_input().set_args(args)
        if 0 == len(args):
            self.print_usage()
        args_result = self.__argparser.parse_args(args)
        self.get_input().set_output_prefix(args_result.output_prefix)
        self.get_input().set_func(args_result.func)
        self.get_input().set_netlist_file_name(args_result.netlist_file)
        if None != args_result.topcell:
            self.get_input().set_topcell_name(args_result.topcell[0])
        if None != args_result.nets:
            self.get_input().set_net_names(args_result.nets)
        if None != args_result.power_nets:
            self.get_input().set_power_net_names(args_result.power_nets)
        if None != args_result.ground_nets:
            self.get_input().set_ground_net_names(args_result.ground_nets)
        self.get_input().set_case_sense(args_result.case)
        self.get_input().set_dollar_comment(args_result.dollar_comment)
        self.get_input().set_debug(args_result.debug)
        self.get_input().set_all_probe(args_result.all_probe)

    def init_log(self):
        self.__log = Log(self.get_input().get_output_prefix())

    def print_inputs(self):
        self.get_log().get_logger().info(f"# print inputs start ... {datetime.datetime.now()}")
        inputs_str = self.get_input().get_inputs_str()
        self.get_log().get_logger().info(f"{inputs_str}")
        self.get_log().get_logger().info(f"# print inputs end ... {datetime.datetime.now()}\n")

    def run_parser(self):
        self.get_log().get_logger().info(f"# run parser start ... {datetime.datetime.now()}")
        my_parser = Parser(self.get_input(), self.get_netlist(), self.get_log())
        my_parser.run()
        # my_parser = run_parser.Parser(self.get_input(), self.get_netlist())
        # my_parser.run()
        # self.set_netlist(my_parser.get_netlist())
        self.get_log().get_logger().info(f"# run parser end ... {datetime.datetime.now()}\n")

    def run_func(self):
        if "makeiprobe" == self.get_input().get_func():
            self.makeiprobe(self.get_input(), self.get_log(), self.get_netlist())
        if "findvnet" == self.get_input().get_func():
            self.findvnet(self.get_input(), self.get_log(), self.get_netlist())

    def makeiprobe(self, t_input, t_log, t_netlist):
        my_makeiprobe = Makeiprobe(t_input, t_log, t_netlist)
        my_makeiprobe.run()

    def findvnet(self, t_input, t_log, t_netlist):
        my_findvnet = Findvnet(t_input, t_log, t_netlist)
        my_findvnet.run()

    def run(self, args):
        self.init_argparser()
        self.read_args(args)
        self.init_log()
        self.get_log().get_logger().info(
            f"# spiceutil({Version().get_program_version()}) start ... {datetime.datetime.now()}\n"
        )
        self.get_log().get_logger().info(f"{Utils().get_system_str('# ')}")
        #
        self.print_inputs()
        #
        if "args" == self.get_input().get_func():
            self.get_log().get_logger().info(
                f"# spiceutil({Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
            )
            self.get_log().get_logger().info(f"# {self.get_performance().get_str()}")
            return
        #
        self.run_parser()
        if "parser" == self.get_input().get_func():
            self.get_log().get_logger().info(
                f"# spiceutil({Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
            )
            self.get_log().get_logger().info(f"# {self.get_performance().get_str()}")
            return
        #
        self.run_func()
        self.get_log().get_logger().info(
            f"# spiceutil({Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
        )
        self.get_log().get_logger().info(f"# {self.get_performance().get_str()}")


def main(args):
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
