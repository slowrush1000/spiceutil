import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from func import Func
from utils import Type_tt
from utils import Utils
from version import Version


class Makeiprobe(Func):
    def __init__(self, t_input=None, t_log=None, t_netlist=None):
        super().__init__(t_input, t_log, t_netlist)

    def makeiprobe(self):
        self.get_log().get_logger().info(f"# makeiprobe start ... {datetime.datetime.now()}")
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_topcell_name(), Type_tt.CELL_CELL
        )
        if None == top_cell:
            self.get_log().get_logger().info(
                f"# error : top cell({self.get_input().get_topcell_name()}) dont exist!"
            )
            self.get_log().get_logger().info(
                f"# error : {self.makeiprobe.__name__}:{inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.get_input().get_net_names():
            self.get_log().get_logger().info(
                f"# makeiprobe({netname}) start ... { datetime.datetime.now()}"
            )
            probe_filename = f"{self.get_input().get_output_prefix()}.{netname}.probe"
            self.get_log().get_logger().info(f"probe file   : {probe_filename}")
            #
            probe_file = open(probe_filename, "wt")
            probe_file.write(f"* {Version().get_program()} - {Version().get_version()}\n")
            probe_file.write(f"* {self.get_input().get_func()} - {datetime.datetime.now()}\n")
            #
            self.makeiprobe_recursive(top_cell, probe_file, netname, "", 0)
            probe_file.write(f"*\n")
            probe_file.close()
            self.get_log().get_logger().info(
                f"# make iprobe({netname}) end ... {
                datetime.datetime.now()}"
            )
        self.get_log().get_logger().info(f"# make iprobe end ... {datetime.datetime.now()}")

    def makeiprobe_recursive(self, parent_cell, probe_file, netname, parent_inst_name, level):
        #
        k_subckt_type_nmos_pmos_mosfet = [
            Type_tt.CELL_CELL_NMOS,
            Type_tt.CELL_CELL_PMOS,
            Type_tt.CELL_NMOS,
            Type_tt.CELL_PMOS,
            Type_tt.CELL_MOSFET,
        ]
        k_subckt_type_nmos_pmos_mosfet_set = set(k_subckt_type_nmos_pmos_mosfet)
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
            if Type_tt.CELL_CELL == cell.get_type():
                self.makeiprobe_recursive(cell, probe_file, netname, inst_name_1, level + 1)
            #
            else:
                node_size = len(inst.get_nodes())
                if False == self.get_input().get_all_probe():
                    if cell.get_type() in k_subckt_type_nmos_pmos_mosfet_set:
                        node_size -= 1
                #
                for pos in range(0, node_size):
                    node = inst.get_node(pos)
                    if netname.lower() == node.get_name().lower():
                        # subckt model :
                        if cell.get_type() in Utils().get_subckt_types_set():
                            self.write_iprobe_subckt_model(probe_file, pos, inst_name_1, cell)
                        else:
                            self.write_iprobe_normal_model(probe_file, pos, inst_name_1)

    def write_iprobe_normal_model(self, probe_file, pos, inst_name):
        probe_file.write(f".probe i{pos + 1}({inst_name})\n")

    def write_iprobe_subckt_model(self, probe_file, pos, inst_name, cell):
        probe_file.write(f".probe x({inst_name}.{cell.get_pins()[pos].get_name()})\n")

    def run(self, args=None):
        self.get_log().get_logger().info(f"# makeiprobe start ... {datetime.datetime.now()}")
        self.makeiprobe()
        self.get_log().get_logger().info(f"# makeiprobe end ... {datetime.datetime.now()}")
