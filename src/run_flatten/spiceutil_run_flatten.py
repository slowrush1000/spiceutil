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


class Flatten(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)

    #    def run_parser(self):
    #        my_parser = run_parser.Parser(self.get_input(), self.get_netlist())
    #        my_parser.run()
    #        self.set_netlist(my_parser.get_netlist())

    def flatten(self):
        self.get_input().get_log().get_logger().info(
            f"# flatten start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.get_input().get_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == top_cell:
            self.get_input().get_log().get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.get_input().get_log().get_logger().info(
                f"# error : {self.make_iprobe.__name__}:{inspect.currentframe().f_lineno})"
            )
            exit()
        #
        flatten_top_cellname = f"{self.get_input().get_top_cellname()}_flatten"
        flatten_top_cell = netlist.Cell(
            flatten_top_cellname, netlist.Type.CELL_CELL
        )
        #
        self.get_input().get_log().get_logger().info(
            f"# flatten end ... {datetime.datetime.now()}"
        )

    def flatten_recursive(
        self,
        flatten_top_cell,
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
            flatten_inst_name = inst.get_name()
            if 0 < level:
                flatten_inst_name = f"{parent_inst_name}{self.get_input().get_flatten_delimiter()}{inst.get_name()}"
            #
            flatten_inst = netlist.Inst(flatten_inst_name, inst.get_type())
            flatten_top_cell.add_inst(flatten_inst_name, flatten_inst)
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
                            node_name_1 = f"{parent_inst_name}{self.get_input().get_flatten_delimiter()}{node.get_name()}"
                        parent_pin_names_1[pos] = node_name_1
            #
            # for pos in range(0, len(inst.get_nodes())):
            #    node = inst.get_node(pos)
            #    netname_1 = netlist.get_netname(parent_pin_names_1[pos])
            #    if netname.lower() == netname_1.lower():
            #        net_result_str.append(
            #            f"{netname} {parent_pin_names_1[pos]}"
            #        )
            #                    self.get_input().get_log().get_logger().debug(
            #                        f"#debug- {pos} {parent_inst_name}.{inst.get_name()} {node.get_name()} {parent_pin_names_1[pos]}"
            #                    )
            #
            cell = inst.get_cell()
            self.flatten_recursive(
                cell,
                net_result_str,
                netname,
                flatten_inst_name,
                parent_pin_names_1,
                level + 1,
            )

    def run(self):
        self.get_input().get_log().get_logger().info(
            f"# flatten start ... {datetime.datetime.now()}\n"
        )
        self.run_parser()
        self.flatten()
        self.get_input().get_log().get_logger().info(
            f"# flatten end ... {datetime.datetime.now()}\n"
        )
