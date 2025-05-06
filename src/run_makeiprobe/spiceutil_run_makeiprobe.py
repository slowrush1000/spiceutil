import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import version
import run


class Makeiprobe(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)

    def makeiprobe(self):
        self.get_input().get_log().get_logger().info(
            f"# makeiprobe start ... {datetime.datetime.now()}\n"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cell_name(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            msg = f"# error: top cell({self.get_top_cell_name()}) don't exist!"
            self.get_input().get_log().get_logger().error("f{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        for net_name in self.get_input().get_net_names():
            self.get_input().get_log().get_logger().info(
                f"# makeiprobe({net_name}) start ... { datetime.datetime.now()}"
            )
            #
            probe_file_name = f"{self.get_input().get_output_prefix()}.{net_name}.makeiprobe.probe"
            self.get_input().get_log().get_logger().info(f"probe file: {probe_file_name}")
            probe_file = self.open_probe_file(probe_file_name)
            #
            parent_node_names = []
            for pin in top_cell.get_pins():
                parent_node_names.append(pin.get_name())
            self.makeiprobe_recursive(probe_file, 0, net_name, top_cell, "", parent_node_names)
            self.close_probe_file(probe_file)
            #
            self.get_input().get_log().get_logger().info(
                f"# make iprobe({net_name}) end ... {datetime.datetime.now()}\n"
            )
        self.get_input().get_log().get_logger().info(
            f"# make iprobe end ... {datetime.datetime.now()}\n"
        )

    def makeiprobe_recursive(
        self, probe_file, level, net_name, parent_cell, parent_inst_name, parent_node_names
    ):
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            inst_name_1 = inst.get_name()
            if 0 < level:
                inst_name_1 = f"{parent_inst_name}.{inst_name_1}"
            #
            node_names_1 = ["*"] * len(inst.get_nodes())
            for pos in range(0, len(inst.get_nodes())):
                node = inst.get_node(pos)
                if netlist.Type.NODE_PIN == node.get_type():
                    node_names_1[pos] = parent_node_names[pos]
                elif node.get_name() in self.get_netlist().get_global_net_names_set():
                    node_names_1[pos] = node.get_name()
                else:
                    node_name_1 = node.get_name()
                    if 0 < level:
                        node_name_1 = f"{parent_inst_name}.{node_name_1}"
                    node_names_1[pos] = node_name_1
            #
            cell = inst.get_cell()
            if netlist.Type.CELL_CELL == cell.get_type():
                self.makeiprobe_recursive(
                    probe_file, level + 1, net_name, cell, inst_name_1, node_names_1
                )
            #
            else:
                if True == self.get_input().get_all_probe():
                    for pos in range(0, len(inst.get_nodes())):
                        node = inst.get_node(pos)
                        if True == self.is_subckt_model(parent_cell, inst):
                            self.write_iprobe_subckt_model(probe_file, pos, inst_name_1, cell)
                        else:
                            self.write_iprobe_normal_model(probe_file, pos, inst_name_1)
                else:
                    for pos in range(0, len(inst.get_nodes())):
                        if net_name == node_names_1[pos]:
                            if True == self.is_subckt_model(parent_cell, inst):
                                self.write_iprobe_subckt_model(probe_file, pos, inst_name_1, cell)
                            else:
                                self.write_iprobe_normal_model(probe_file, pos, inst_name_1)

    def is_subckt_model(self, parent_cell, inst):
        if parent_cell.get_name() == inst.get_cell().get_name():
            if netlist.Type.CELL_CELL == parent_cell.get_type():
                if inst.get_cell().get_type() in netlist.k_SUBCKT_MODEL_SET():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def write_iprobe_normal_model(self, probe_file, pos, inst_name):
        probe_file.write(f".probe i{pos + 1}({inst_name})\n")

    def write_iprobe_subckt_model(self, probe_file, pos, inst_name, cell):
        probe_file.write(f".probe x({inst_name}.{cell.get_pins()[pos].get_name()})\n")

    def open_probe_file(self, probe_file_name):
        probe_file = open(probe_file_name, "wt")
        probe_file.write(f"*\n")
        probe_file.write(
            f"* {version.Version().get_program()} - {version.Version().get_version()}\n"
        )
        probe_file.write(f"* {self.get_input().get_run()} - {datetime.datetime.now()}\n")
        probe_file.write(f"*\n")
        return probe_file

    def close_probe_file(self, probe_file):
        probe_file.write(f"*\n")
        probe_file.close()

    def run(self, args=None):
        self.makeiprobe()
