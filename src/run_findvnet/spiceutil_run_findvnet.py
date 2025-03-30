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
import run_parser


class Findvnet(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)

    # def run_parser(self):
    #    my_parser = run_parser.Parser(self.get_input(), self.get_netlist())
    #    my_parser.run()
    #    self.set_netlist(my_parser.get_netlist())

    def findvnet(self):
        self.get_input().get_log().get_logger().info(
            f"# findvnet start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            self.get_input().get_log().get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.get_input().get_log().get_logger().info(
                f"# error : {self.make_iprobe.__name__}:{
                inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.get_input().get_netnames():
            #
            net_result_str = []
            #
            self.get_input().get_log().get_logger().info(
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
            self.get_input().get_log().get_logger().info(
                f"findvnet({netname}) end ... {
               datetime.datetime.now()}"
            )
        #
        self.get_input().get_log().get_logger().info(
            f"# findvnet end ... {datetime.datetime.now()}"
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
                    self.get_input().get_log().get_logger().debug(
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
        self.get_input().get_log().get_logger().info(
            f"vnet file : {probe_filename}"
        )
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
        self.get_input().get_log().get_logger().info(
            f"# findvnet start ... {datetime.datetime.now()}\n"
        )
        self.run_parser()
        self.findvnet()
        self.get_input().get_log().get_logger().info(
            f"# findvnet end ... {datetime.datetime.now()}\n"
        )
