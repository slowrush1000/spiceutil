import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import run_parser
import version


class Makeiprobe:
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

    def run_parser(self):
        my_parser = run_parser.Parser(self.get_input().get_log())
        my_parser.set_input(self.get_input())
        my_parser.run()
        self.set_netlist(my_parser.get_netlist())

    def makeiprobe(self):
        self.get_logger().info(
            f"# makeiprobe start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            self.get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.get_logger().info(
                f"# error : {self.makeiprobe.__name__}:{
                inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.get_input().get_netnames():
            self.get_logger().info(
                f"# makeiprobe({netname}) start ... { datetime.datetime.now()}"
            )
            probe_filename = (
                f"{self.get_input().get_output_prefix()}.{netname}.probe"
            )
            self.get_logger().info(f"probe file   : {probe_filename}")
            #
            probe_file = open(probe_filename, "wt")
            probe_file.write(
                f"* {version.Version().get_program()} - {version.Version().get_version()}\n"
            )
            probe_file.write(
                f"* {self.get_input().get_run()} - {datetime.datetime.now()}\n"
            )
            #
            self.makeiprobe_recursive(top_cell, probe_file, netname, "", 0)
            probe_file.write(f"*\n")
            probe_file.close()
            self.get_logger().info(
                f"# make iprobe({netname}) end ... {
                datetime.datetime.now()}"
            )
        self.get_logger().info(
            f"# make iprobe end ... {datetime.datetime.now()}"
        )

    def makeiprobe_recursive(
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
                self.makeiprobe_recursive(
                    cell, probe_file, netname, inst_name_1, level + 1
                )
            #
            else:
                node_size = inst.get_node_size()
                if False == self.get_input().get_all_probe():
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
        self.get_logger().info(
            f"# makeiprobe start ... {datetime.datetime.now()}"
        )
        self.run_parser()
        self.makeiprobe()
        self.get_logger().info(
            f"# makeiprobe end ... {datetime.datetime.now()}"
        )
