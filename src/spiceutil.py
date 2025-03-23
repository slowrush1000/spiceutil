import sys
import datetime
import input
import logging
import log
import run_makeiprobe
import run_findvnet
import netlist
import run_parser
import time
import tomllib
import version
import psutil


class Spiceutil:
    def __init__(self):
        self.m_input = input.Input()

    def set_input(self, input_t):
        self.m_input = input_t

    def get_input(self):
        return self.m_input

    def print_usage(self):
        print(
            f"{version.Version().get_program()} {version.Version().get_version()}"
        )
        print(f"spiceutil.py usage:")
        print(f"% spiceutil.py output_prefix config_file")

    def find_get_output_prefix(self, args):
        if 3 != len(args):
            self.print_usage()
            exit()
        self.get_input().set_output_prefix(args[1])

    def init_log(self):
        my_log = log.Log(self.get_input().get_output_prefix())
        self.get_input().set_log(my_log)

    def print_input(self):
        self.get_input().get_log().get_logger().info(
            f"# print input start ... {datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
            f"{self.get_input().get_str()}"
        )
        self.get_input().get_log().get_logger().info(
            f"# print input end ... {datetime.datetime.now()}\n"
        )

    def read_args(self, args):
        self.get_input().get_log().get_logger().info(
            f"# read args start ... {datetime.datetime.now()}"
        )
        if 3 != len(args):
            self.print_usage()
            exit()
        self.get_input().set_output_prefix(args[1])
        self.get_input().set_config_filename(args[2])
        self.get_input().set_args(args)
        self.get_input().get_log().get_logger().info(
            f"# read args end ... {datetime.datetime.now()}\n"
        )

    def read_config_file(self):
        self.get_input().get_log().get_logger().info(
            f"# read config file({self.get_input().get_config_filename()}) start ... {datetime.datetime.now()}"
        )
        #
        with open(self.get_input().get_config_filename(), "rb") as config_file:
            config = tomllib.load(config_file)
            #
            if "run" in config:
                self.get_input().set_run(config["run"])
            if "spice_file" in config:
                self.get_input().set_spice_filename(config["spice_file"])
            if "top_cell" in config:
                self.get_input().set_top_cellname(config["top_cell"])
            if "netnames" in config:
                self.get_input().set_netnames(config["netnames"].split())
            if "casesensitive" in config:
                self.get_input().set_casesensitive(config["casesensitive"])
            if "dolar_comment" in config:
                self.get_input().set_dollar_comment(config["dolar_comment"])
            if "all_probe" in config:
                self.get_input().set_all_probe(config["all_probe"])
            if "is_write_1st_spc" in config:
                self.get_input().set_is_write_1st_spc(
                    config["is_write_1st_spc"]
                )
            if "is_write_2nd_spc" in config:
                self.get_input().set_is_write_2nd_spc(
                    config["is_write_2nd_spc"]
                )
            if "log_verbose" in config:
                self.get_input().set_log_verbose(config["log_verbose"])
                self.get_input().get_log().set_level(config["log_verbose"])
            if "text_width" in config:
                self.get_input().set_text_width(int(config["text_width"]))
        #
        self.get_input().get_log().get_logger().info(
            f"# read config file({self.get_input().get_config_filename()}) end ... {datetime.datetime.now()}\n"
        )

    def run(self, args):
        time_start = time.time()
        #
        self.find_get_output_prefix(args)
        self.init_log()
        self.get_input().get_log().get_logger().info(
            f"# {version.Version().get_program()} {version.Version().get_version()} start ... {datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
            f"{self.get_input().get_system_str()}\n"
        )
        self.read_args(args)
        self.read_config_file()
        self.print_input()
        #
        match self.get_input().get_run():
            case "config":
                pass
            case "parser":
                my_parser = run_parser.Parser(
                    self.get_input(), netlist.Netlist()
                )
                my_parser.run()
            case "findvnet":
                my_findvnet = run_findvnet.Findvnet(
                    self.get_input(), netlist.Netlist()
                )
                my_findvnet.run()
            case "makeiprobe":
                my_makeiprobe = run_makeiprobe.Makeiprobe(
                    self.get_input(), self.get_input().get_log().get_logger()
                )
                my_makeiprobe.run()

        #
        self.get_input().get_log().get_logger().info(
            f"# {version.Version().get_program()} {version.Version().get_version()} end ... {datetime.datetime.now()}\n"
        )
        time_end = time.time()
        self.get_input().get_log().get_logger().info(
            f"# cpu time : {time.process_time_ns()/1.0e9:.3f} sec, wall time : {(time_end - time_start):.3f} sec"
        )
        self.get_input().get_log().get_logger().info(
            f"# memory usage(rss) : {psutil.Process().memory_info().rss/1000.0/1000.0:.1f} mb"
        )


def main(args):
    my_spiceutil = Spiceutil()
    my_spiceutil.run(args)


if __name__ == "__main__":
    main(sys.argv)
