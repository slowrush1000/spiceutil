import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import log
import netlist
import version
import run


class Findvnet(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)

    def findvnet(self):
        self.get_input().get_log().get_logger().info(
            f"# findvnet start ... {datetime.datetime.now()}\n"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cell_name(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            msg = f"# error: top cell({self.get_input().get_top_cell_name()}) don't exist!"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        for net_name in self.get_input().get_net_names():
            self.get_input().get_log().get_logger().info(
                f"findvnet({net_name}) start ... {
                datetime.datetime.now()}"
            )
            #
            parent_pin_names = []
            for pos in range(0, len(top_cell.get_pins())):
                pin = top_cell.get_pin(pos)
                parent_pin_names.append(pin.get_name())
            #
            net_result_dic = {}  # key : net_name(local), data : net_name(full)'s set
            #
            self.find_vnet_recursive(top_cell, net_result_dic, net_name, "", parent_pin_names, 0)
            #
            self.write_findvnet_file(net_name, net_result_dic)
            self.get_input().get_log().get_logger().info(
                f"findvnet({net_name}) end ... {datetime.datetime.now()}\n"
            )
        #
        self.get_input().get_log().get_logger().info(
            f"# findvnet end ... {datetime.datetime.now()}"
        )

    def find_vnet_recursive(
        self,
        parent_cell,
        net_result_dic,
        net_name,
        parent_inst_name,
        parent_pin_names,
        level,
    ):
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
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
                    # global net_name
                    if None != self.get_netlist().get_global_net_names_set():
                        if node_name_1 in self.get_netlist().get_global_net_names_set():
                            parent_pin_names_1[pos] = node_name_1
                        else:
                            if 0 < level:
                                node_name_1 = f"{parent_inst_name}.{node.get_name()}"
                            parent_pin_names_1[pos] = node_name_1
                    else:
                        if 0 < level:
                            node_name_1 = f"{parent_inst_name}.{node.get_name()}"
                        parent_pin_names_1[pos] = node_name_1
            #
            for pos in range(0, len(inst.get_nodes())):
                net_name_local = netlist.get_net_name(parent_pin_names_1[pos])
                if True == netlist.is_equal(
                    net_name, net_name_local, self.get_input().get_casesensitive()
                ):
                    #
                    if not net_name_local in net_result_dic:
                        net_name_full_set = set([parent_pin_names_1[pos]])
                        net_result_dic[net_name_local] = net_name_full_set
                    else:
                        net_name_full_set = net_result_dic[net_name_local]
                        if not parent_pin_names_1[pos] in net_name_full_set:
                            net_name_full_set.add(parent_pin_names_1[pos])
                    #
            #
            cell = inst.get_cell()
            self.find_vnet_recursive(
                cell,
                net_result_dic,
                net_name,
                inst_name_1,
                parent_pin_names_1,
                level + 1,
            )

    def write_findvnet_file(self, net_name, net_result_dic):
        findvnet_file_name = f"{self.get_input().get_output_prefix()}.{net_name}.findvnet.txt"
        #
        self.get_input().get_log().get_logger().info(f"vnet file : {findvnet_file_name}")
        findvnet_file = open(findvnet_file_name, "wt")
        #
        findvnet_file.write(
            f"* {version.Version().get_program()} - {version.Version().get_version()}\n"
        )
        findvnet_file.write(f"* {self.get_input().get_run()} - {datetime.datetime.now()}\n")
        findvnet_file.write(f"* net : {net_name}\n")
        findvnet_file.write(f"* net_name net_name(local) net_name(full)\n")
        #
        for net_name_local in net_result_dic:
            net_name_fulls = net_result_dic[net_name_local]
            for net_name_full in net_name_fulls:
                findvnet_file.write(f"{net_name} {net_name_local} {net_name_full}\n")
        #
        findvnet_file.write(f"*\n")
        findvnet_file.close()

    def run(self):
        # self.get_input().get_log().get_logger().info(
        #    f"# findvnet start ... {datetime.datetime.now()}\n"
        # )
        self.findvnet()
        # self.get_input().get_log().get_logger().info(
        #    f"# findvnet end ... {datetime.datetime.now()}\n"
        # )
