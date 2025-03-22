import argparse
import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import parser


class Makeiprobe:
    def __init__(self, log=None):
        super().__init__(log)
        self.m_netnames = []
        self.m_top_cellname = netlist.k_TOP_CELLNAME
        self.m_all_probe = False
        self.m_dollar_comment = True
        self.m_arg_parser = argparse.ArgumentParser()

    def set_netnames(self, netnames):
        self.m_netnames = netnames

    def get_netnames(self):
        return self.m_netnames

    def set_top_cellname(self, top_cellname):
        self.m_top_cellname = top_cellname

    def get_top_cellname(self):
        return self.m_top_cellname

    def set_all_probe(self, all_probe):
        self.m_all_probe = all_probe

    def get_all_probe(self):
        return self.m_all_probe

    def set_dollar_comment(self, dollar_comment):
        self.m_dollar_comment = dollar_comment

    def get_dollar_comment(self):
        return self.m_dollar_comment

    def read_args(self, args=None):
        self.get_log().get_logger().info(
            f"# read args start ... {datetime.datetime.now()}"
        )
        #
        self.m_arg_parser.add_argument("output_prefix")
        self.m_arg_parser.add_argument("run")
        self.m_arg_parser.add_argument("filename")
        self.m_arg_parser.add_argument(
            "-net", action="extend", nargs="+", type=str
        )
        self.m_arg_parser.add_argument(
            "-top_cell", default=netlist.k_TOP_CELLNAME
        )
        self.m_arg_parser.add_argument(
            "-all_probe", action="store_true", default=False
        )
        self.m_arg_parser.add_argument(
            "-disable_dollar_comment", action="store_false", default=True
        )
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
        self.set_run(netlist.Run.MAKEIPROBE)
        self.set_netnames(args_1.net)
        self.set_top_cellname(args_1.top_cell)
        self.set_all_probe(args_1.all_probe)
        self.set_dollar_comment(args_1.disable_dollar_comment)
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
        self.get_log().get_logger().info(
            f"file             : {self.get_filename()}"
        )
        self.get_log().get_logger().info(
            f"run              : {self.get_run()}"
        )
        for netname in self.get_netnames():
            self.get_log().get_logger().info(f"net              : {netname}")
        self.get_log().get_logger().info(
            f"top cell         : {self.get_top_cellname()}"
        )
        self.get_log().get_logger().info(
            f"all probe        : {self.get_all_probe()}"
        )
        self.get_log().get_logger().info(
            f"dollar comment   : {self.get_dollar_comment()}"
        )
        self.get_log().get_logger().info(
            f"# print inputs end ... {datetime.datetime.now()}"
        )

    def run_parser(self):
        my_parser = parser.Parser(self.get_log())
        my_parser.set_filename(self.get_filename())
        my_parser.set_dollar_comment(self.get_dollar_comment())
        my_parser.run()
        self.set_netlist(my_parser.get_netlist())

    def make_iprobe(self):
        self.get_log().get_logger().info(
            f"# make iprobe start ... {datetime.datetime.now()}"
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
        for netname in self.get_netnames():
            self.m_log.get_logger().info(
                f"# make iprobe({netname}) start ... {
                datetime.datetime.now()}"
            )
            probe_filename = f"{self.get_output_prefix()}.{netname}.probe"
            self.m_log.get_logger().info(f"probe file   : {probe_filename}")
            #
            probe_file = open(probe_filename, "wt")
            probe_file.write(
                f"* {netlist.get_program()} - {netlist.get_version()}\n"
            )
            probe_file.write(
                f"* {self.get_run()} - {datetime.datetime.now()}\n"
            )
            #
            self.make_iprobe_recursive(top_cell, probe_file, netname, "", 0)
            probe_file.write(f"*\n")
            probe_file.close()
            self.m_log.get_logger().info(
                f"# make iprobe({netname}) end ... {
                datetime.datetime.now()}"
            )
        self.get_log().get_logger().info(
            f"# make iprobe end ... {datetime.datetime.now()}"
        )

    def make_iprobe_recursive(
        self, parent_cell, probe_file, netname, parent_inst_name, level
    ):
        #
        k_subckt_type_nmos_pmos_mosfet = [
            netlist.Type.CELL_CELL_NMOS,
            netlist.Type.CELL_CELL_PMOS,
            netlist.Type.CELL_NMOS,
            netlist.Type.CELL_PMOS,
            netlist.Type.CELL_MOSFET,
        ]
        k_subckt_type_nmos_pmos_mosfet_set = set(
            k_subckt_type_nmos_pmos_mosfet
        )
        #
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            #
            inst_name_1 = inst_name
            if 0 < level:
                inst_name_1 = f"{parent_inst_name}.{inst_name_1}"
            #
            cell = inst.get_cell()
            #
            if netlist.Type.CELL_CELL == cell.get_type():
                self.make_iprobe_recursive(
                    cell, probe_file, netname, inst_name_1, level + 1
                )
            #
            else:
                node_size = inst.get_node_size()
                if False == self.get_all_probe():
                    if cell.get_type() in k_subckt_type_nmos_pmos_mosfet_set:
                        node_size -= 1
                #
                for pos in range(0, node_size):
                    node = inst.get_node(pos)
                    if netname.lower() == node.get_name().lower():
                        # subckt model :
                        if cell.get_type() in netlist.k_SUBCKT_TYPES_SET:
                            self.write_iprobe_subckt_model(
                                probe_file, pos, inst_name_1, cell
                            )
                        else:
                            self.write_iprobe_normal_model(
                                probe_file, pos, inst_name_1
                            )

    def write_iprobe_normal_model(self, probe_file, pos, inst_name):
        probe_file.write(f".probe i{pos + 1}({inst_name})\n")

    def write_iprobe_subckt_model(self, probe_file, pos, inst_name, cell):
        probe_file.write(
            f".probe x({inst_name}.{cell.get_pins()[pos].get_name()})\n"
        )

    def run(self, args=None):
        self.get_log().get_logger().info(
            f"# make_iprobe start ... {datetime.datetime.now()}"
        )
        self.read_args(args)
        self.print_inputs()
        self.run_parser()
        self.make_iprobe()
        self.get_log().get_logger().info(
            f"# make_iprobe end ... {datetime.datetime.now()}"
        )
