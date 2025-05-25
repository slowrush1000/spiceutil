import argparse
import datetime
import os
import sys

#
import input
import log
import makeiprobe
import version


class Spiceutil:
    def __init__(self):
        self.__argparser = None
        self.__input = input.Input()
        #
        self.__argparser = None
        self.__log = None

    def get_input(self):
        return self.__input

    def run(self, args):
        self.init_argparser()
        self.read_args(args)
        self.init_log()
        self.__log.get_logger().info(
            f"# spiceutil({version.Version().get_program_version()}) start ... {datetime.datetime.now()}\n"
        )
        self.print_inputs()
        self.run_func()
        self.__log.get_logger().info(
            f"# spiceutil({version.Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
        )

    def print_usage(self):
        print(f"spiceutil({version.Version().get_program_version()}) usage:")
        print(
            f"spiceutil output_prefix makeiprobe netlist_file < -topcell topcell > < -nets netname1 ...> "
        )
        print(
            f"spiceutil output_prefix findvnet   netlist_file < -topcell topcell > < -nets netname1 ...>"
        )
        print(
            f"spiceutil output_prefix flatten    netlist_file < -topcell topcell > < -nets netname1 ...>"
        )
        print(
            f"spiceutil output_prefix finddecap  netlist_file < -topcell topcell > < -power_nets netname1 ... > < -ground_nets netname1 ... >"
        )

    def init_argparser(self):
        self.__argparser = argparse.ArgumentParser(
            description=f"spiceutil({version.Version().get_program_version()}"
        )
        self.__argparser.add_argument(
            "output_prefix", type=str, help="output prefix, ex) ${output_prefix}.log"
        )
        self.__argparser.add_argument(
            "func", type=str, help="func, ex) makeiprobe, findvent, flatten, finddecap"
        )
        self.__argparser.add_argument("netlist_file", type=str, help="ckt file")
        self.__argparser.add_argument("-topcell", type=str, nargs=1, help="top cell name")
        self.__argparser.add_argument("-nets", type=str, nargs="*", help="netnames")
        self.__argparser.add_argument(
            "-power_nets", type=str, nargs="*", help="power netnames"
        )
        self.__argparser.add_argument(
            "-ground_nets", type=str, nargs="*", help="ground netnames"
        )
        self.__argparser.add_argument("-verbose", type=bool)

    def read_args(self, args):
        self.get_input().set_args(args)
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

    def init_log(self):
        self.__log = log.Log(self.get_input().get_output_prefix())

    def print_inputs(self):
        self.__log.get_logger().info(
            f"# print inputs start ... {datetime.datetime.now()}"
        )
        inputs_str = self.get_input().get_inputs_str()
        self.__log.get_logger().info(f"{inputs_str}")
        self.__log.get_logger().info(f"# print inputs end ... {datetime.datetime.now()}")

    def run_func(self):
        if "makeiprobe" == self.get_input().get_func():
            self.makeiprobe(self.get_input(), self.get_log())

    def makeiprobe(self):
        my_makeiprobe = makeiprobe.Makeiprobe()
        my_makeiprobe.run()


def main(args):
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
