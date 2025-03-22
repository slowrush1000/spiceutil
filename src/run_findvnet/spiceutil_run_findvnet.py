import argparse
import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import netlist
import log
import parser
import version


class Findvnet:
    def __init__(self, input=None, logger=None):
        self.m_input = input
        self.m_logger = logger
        self.m_netlist = None

    def set_input(self, input):
        self.m_input = input

    def get_input(self):
        return self.m_input

    def set_logger(self, logger):
        self.m_logger = logger

    def get_logger(self):
        return self.m_logger

    def set_netlist(self, netlist):
        self.m_netlist = netlist

    def get_netlist(self):
        return self.m_netlist

    #    def read_args(self, args=None):
    #        self.get_log().get_logger().info(
    #            f"# read args start ... {datetime.datetime.now()}"
    #        )
    #        #
    #        self.m_arg_parser.add_argument("output_prefix")
    #        self.m_arg_parser.add_argument("filename")
    #        self.m_arg_parser.add_argument("run")
    #        self.m_arg_parser.add_argument(
    #            "-net", action="extend", nargs="+", type=str
    #        )
    #        self.m_arg_parser.add_argument(
    #            "-top_cell", default=netlist.k_TOP_CELLNAME
    #        )
    #        #
    #        args_1 = None
    #        if None != self.get_log():
    #            self.get_log().get_logger().info(f"args : {' '.join(args)}")
    #        else:
    #            print(f"args : {' '.join(args)}")
    #        #
    #        if None == args:
    #            args_1 = self.m_arg_parser.parse_args()
    #        else:
    #            args_1 = self.m_arg_parser.parse_args(args)
    #        #
    #        self.set_output_prefix(args_1.output_prefix)
    #        self.set_filename(args_1.filename)
    #        self.set_run(netlist.Run.FINDVNET)
    #        self.set_netnames(args_1.net)
    #        self.set_top_cellname(args_1.top_cell)
    #        self.get_log().get_logger().info(
    #            f"# read args end ... {datetime.datetime.now()}"
    #        )
    #
    #    def print_inputs(self):
    #        self.get_log().get_logger().info(
    #            f"# print inputs start ... {datetime.datetime.now()}"
    #        )
    #        self.get_log().get_logger().info(
    #            f"output_prefix    : {self.get_output_prefix()}"
    #        )
    #        self.get_log().get_logger().info(
    #            f"file             : {self.get_filename()}"
    #        )
    #        self.get_log().get_logger().info(
    #            f"run              : {self.get_run()}"
    #        )
    #        for netname in self.get_netnames():
    #            self.get_log().get_logger().info(f"net              : {netname}")
    #        self.get_log().get_logger().info(
    #            f"top cell         : {self.get_top_cellname()}"
    #        )
    #        self.get_log().get_logger().info(
    #            f"# print inputs end ... {datetime.datetime.now()}"
    #        )

    def run_parser(self):
        my_parser = parser.Parser(self.get_input().get_log())
        my_parser.set_input(self.get_input())
        my_parser.set_log(self.get_input().get_log())
        my_parser.run()
        self.set_netlist(my_parser.get_netlist())

    def findvnet(self):
        self.get_logger().info(
            f"# findvnet start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            self.get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.get_logger().info(
                f"# error : {self.make_iprobe.__name__}:{
                inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.get_input().get_netnames():
            #
            net_result_str = []
            #
            self.get_logger().info(
                f"findvnet({netname}) start ... {
                datetime.datetime.now()}"
            )
            parent_pin_names = []
            for pos in range(0, len(top_cell.get_pins())):
                pin = top_cell.get_pin(pos)
                parent_pin_names.append(pin.get_name())
            self.find_vnet_recursive(
                top_cell, net_result_str, netname, "", parent_pin_names, 0
            )
            self.write_findvnet_file(netname, net_result_str)
            self.get_logger().info(
                f"findvnet({netname}) end ... {
               datetime.datetime.now()}"
            )

    def find_vnet_recursive(
        self,
        parent_cell,
        net_result_str,
        netname,
        parent_inst_name,
        parent_pin_names,
        level,
    ):
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            #
            inst_name_1 = inst.get_name()
            if 0 < level:
                inst_name_1 = f"{parent_inst_name}.{inst.get_name()}"
            #
            parent_pin_names_1 = ["*"] * len(inst.get_nodes())
            for pos in range(0, len(inst.get_nodes())):
                node = inst.get_node(pos)
                if netlist.Type.NODE_PIN == node.get_type():
                    parent_pin_names_1[pos] = parent_pin_names[pos]
                else:
                    node_name_1 = f"{node.get_name()}"
                    # global netname
                    if None != self.get_netlist().get_global_netnames_set():
                        if (
                            node_name_1
                            in self.get_netlist().get_global_netnames_set()
                        ):
                            parent_pin_names_1[pos] = node_name_1
                        else:
                            if 0 < level:
                                node_name_1 = (
                                    f"{parent_inst_name}.{node.get_name()}"
                                )
                            parent_pin_names_1[pos] = node_name_1
                    else:
                        if 0 < level:
                            node_name_1 = (
                                f"{parent_inst_name}.{node.get_name()}"
                            )
                        parent_pin_names_1[pos] = node_name_1
            #
            for pos in range(0, len(inst.get_nodes())):
                node = inst.get_node(pos)
                netname_1 = netlist.get_netname(parent_pin_names_1[pos])
                if netname.lower() == netname_1.lower():
                    net_result_str.append(
                        f"{netname} {parent_pin_names_1[pos]}"
                    )
                    self.get_logger().debug(
                        f"#debug- {pos} {parent_inst_name}.{inst.get_name()} {node.get_name()} {parent_pin_names_1[pos]}"
                    )
            #
            cell = inst.get_cell()
            self.find_vnet_recursive(
                cell,
                net_result_str,
                netname,
                inst_name_1,
                parent_pin_names_1,
                level + 1,
            )

    def write_findvnet_file(self, netname, net_result_str):
        net_result_str_set = set(net_result_str)
        net_result_str_1 = list(net_result_str_set)
        probe_filename = (
            f"{self.get_input().get_output_prefix()}.{netname}.findvnet.txt"
        )
        self.get_logger().info(f"vnet file : {probe_filename}")
        probe_file = open(probe_filename, "wt")
        probe_file.write(
            f"* {version.Version().get_program()} - {version.Version().get_version()}\n"
        )
        probe_file.write(
            f"* {self.get_input().get_run()} - {datetime.datetime.now()}\n"
        )
        probe_file.write(f"* net : {netname}\n")
        for net_result in net_result_str_1:
            probe_file.write(f"{net_result}\n")
        probe_file.write(f"*\n")
        probe_file.close()

    def run(self):
        self.get_logger().info(
            f"# findvnet start ... {datetime.datetime.now()}\n"
        )
        self.run_parser()
        self.findvnet()
        self.get_logger().info(
            f"# findvnet end ... {datetime.datetime.now()}\n"
        )
