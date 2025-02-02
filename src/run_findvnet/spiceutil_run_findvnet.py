import argparse
import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import parser
import run


class Findvnet(run.Run):
    def __init__(self, log=None):
        super().__init__(log)
        self.m_netnames = []
        self.m_top_cellname = netlist.k_TOP_CELLNAME
        self.m_arg_parser = argparse.ArgumentParser()

    def set_netnames(self, netnames):
        self.m_netnames = netnames

    def get_netnames(self):
        return self.m_netnames

    def set_top_cellname(self, top_cellname):
        self.m_top_cellname = top_cellname

    def get_top_cellname(self):
        return self.m_top_cellname

    def read_args(self, args=None):
        self.get_log().get_logger().info(
            f"# read args start ... {datetime.datetime.now()}"
        )
        #
        self.m_arg_parser.add_argument("output_prefix")
        self.m_arg_parser.add_argument("run")
        self.m_arg_parser.add_argument("filename")
        self.m_arg_parser.add_argument("-net", action="extend", nargs="+", type=str)
        self.m_arg_parser.add_argument("-top_cell", default=netlist.k_TOP_CELLNAME)
        #
        args_1 = None
        if None != self.get_log():
            self.get_log().get_logger().info(f"args : {' '.join(args)}")
        else:
            print(f"args : {' '.join(args)}")
        #
        if None == args:
            args_1 = self.m_arg_parser.parse_args()
        else:
            args_1 = self.m_arg_parser.parse_args(args)
        #
        self.set_output_prefix(args_1.output_prefix)
        self.set_filename(args_1.filename)
        self.set_run(netlist.Run.FINDDECAP)
        self.set_netnames(args_1.net)
        self.set_top_cellname(args_1.top_cell)
        self.get_log().get_logger().info(
            f"# read args end ... {datetime.datetime.now()}"
        )

    def print_inputs(self):
        self.get_log().get_logger().info(
            f"# print inputs start ... {datetime.datetime.now()}"
        )
        self.get_log().get_logger().info(
            f"output_prefix    : {self.get_output_prefix()}"
        )
        self.get_log().get_logger().info(f"file             : {self.get_filename()}")
        self.get_log().get_logger().info(f"run              : {self.get_run()}")
        for netname in self.get_netnames():
            self.get_log().get_logger().info(f"net              : {netname}")
        self.get_log().get_logger().info(
            f"top cell         : {self.get_top_cellname()}"
        )
        self.get_log().get_logger().info(
            f"# print inputs end ... {datetime.datetime.now()}"
        )

    def run_parser(self):
        my_parser = parser.Parser(self.get_log())
        my_parser.set_filename(self.get_filename())
        my_parser.run()
        self.set_netlist(my_parser.get_netlist())

    def find_vnet(self):
        self.get_log().get_logger().info(
            f"# find vnet start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            self.m_log.get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.m_log.get_logger().info(
                f"# error : {self.make_iprobe.__name__}:{
                inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.get_netnames():
            self.m_log.get_logger().info(
                f"# find vnet({netname}) start ... {
                datetime.datetime.now()}"
            )
            probe_filename = f"{self.get_output_prefix()}.{netname}.findvnet.txt"
            self.m_log.get_logger().info(f"vnet file    : {probe_filename}")
            #
            probe_file = open(probe_filename, "wt")
            probe_file.write(f"* {netlist.get_program()} - {netlist.get_version()}\n")
            probe_file.write(f"* {self.get_run()} - {datetime.datetime.now()}\n")
            #
            self.find_vnet_recursive(top_cell, probe_file, netname, "", 0)
            probe_file.write(f"*\n")
            probe_file.close()
            self.m_log.get_logger().info(
                f"# find vnet({netname}) end ... {
                datetime.datetime.now()}"
            )
        self.get_log().get_logger().info(
            f"# find vnet end ... {datetime.datetime.now()}"
        )

    def find_vnet_recursive(
        self, parent_cell, probe_file, netname, parent_inst_name, level
    ):
        for node_name in parent_cell.get_node_dic():
            node = parent_cell.get_node_dic()[node_name]
            if netname.lower() == node.get_name().lower():
                node_name_1 = node.get_name()
                if netlist.Type.NODE_PIN != node.get_type():
                    node_name_1 = f"{parent_inst_name}.{node.get_name()}"
                probe_file.write(f"{netname} {node_name_1}")
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            cell = inst.get_cell()
            if netlist.Type.CELL_CELL == cell.get_type():
                self.find_vnet_recursive(
                    cell,
                    probe_file,
                    netname,
                )

    def run(self, args=None):
        self.get_log().get_logger().info(
            f"# make_iprobe start ... {datetime.datetime.now()}"
        )
        self.read_args(args)
        self.print_inputs()
        self.run_parser()
        self.find_vnet()
        self.get_log().get_logger().info(
            f"# make_iprobe end ... {datetime.datetime.now()}"
        )
