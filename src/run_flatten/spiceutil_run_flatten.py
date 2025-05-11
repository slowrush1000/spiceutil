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


class flatten(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)

    def flatten(self):
        top_cell = self.get_netlist().get_cell(self.get_input().get_top_cellname(), netlist.Type.CELL_CELL)
        if None == top_cell:
            self.get_input().get_log().get_logger().info(f"# error : top cell({self.get_top_cellname()}) dont exist!")
            self.get_input().get_log().get_logger().info(
                f"# error : {self.flatten.__name__}:{inspect.currentframe().f_lineno})"
            )
            exit()
        #
        parent_inst_name = f""
        parent_pin_names = []
        for pin in top_cell.get_pins():
            pinname = pin.get_name()
            parent_pin_names.append(pinname)
        #
        flatten_filename = f"{self.get_input().get_output_prefix()}.{top_cell.get_name()}.flatten.spc"
        self.get_input().get_log().get_logger().info(f"# flatten file : {flatten_filename}")
        flatten_file = open(flatten_filename, "wt")
        #
        self.flatten_recursive(flatten_file, top_cell, parent_inst_name, parent_pin_names, 0)
        #
        flatten_file.close()

    def flatten_recursive(
        self,
        flatten_file,
        parent_cell,
        parent_inst_name,
        parent_pin_names,
        level,
    ):
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            # flatten inst를 만든다.
            flatten_inst_name = inst.get_name()
            if 0 < level:
                flatten_inst_name = f"{parent_inst_name}{self.get_input().get_flatten_delimiter()}{inst.get_name()}"
            # flatten inst node를 만든다.
            flatten_inst_node_names = ["*"] * len(inst.get_nodes())
            for pos in range(0, len(inst.get_nodes())):
                node = inst.get_node(pos)
                if netlist.Type.NODE_PIN == node.get_type():
                    flatten_inst_node_names[pos] = parent_pin_names[pos]
                else:
                    node_name_1 = f"{node.get_name()}"
                    # global nodename
                    if node_name_1 in self.get_netlist().get_global_netnames_set():
                        flatten_inst_node_names[pos] = node_name_1
                    # local nodename
                    else:
                        node_name_1 = self.make_flatten_name(parent_inst_name, node_name_1, level)
                        flatten_inst_node_names[pos] = node_name_1
            #
            if netlist.Type.CELL_CELL == inst.get_cell().get_type():
                self.flatten_recursive(
                    flatten_file,
                    inst.get_cell(),
                    flatten_inst_name,
                    flatten_inst_node_names,
                    level + 1,
                )
            else:
                self.write_flatten_inst_line(flatten_file, flatten_inst_name, flatten_inst_node_names, inst, level)

    def make_flatten_name(self, parent_inst_name, name, level):
        if 0 < level:
            return f"{parent_inst_name}{self.get_input().get_flatten_delimiter()}{name}"
        else:
            return name

    def write_flatten_inst_line(self, flatten_file, flatten_inst_name, flatten_inst_node_names, inst, level):
        # s1 = self.get_netlist_str(flatten_inst_name, flatten_inst_node_names, inst)
        # flatten_file.write(f"{s1}\n")
        pass

    def run(self):
        self.get_input().get_log().get_logger().info(f"# flatten start ... {datetime.datetime.now()}\n")
        self.run_parser()
        self.flatten()
        self.get_input().get_log().get_logger().info(f"# flatten end ... {datetime.datetime.now()}\n")


#    def get_netlist_str(self, flatten_inst_name, flatten_inst_node_names, inst):
#        match inst.get_type():
#            case netlist.Type.INST_R:
#                return self.get_netlist_str_r(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_L:
#                return self.get_netlist_str_l(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_C:
#                return self.get_netlist_str_c(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_K:
#                return self.get_netlist_str_k(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_VS:
#                return self.get_netlist_str_vs(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_CS:
#                return self.get_netlist_str_cs(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_VCVS:
#                return self.get_netlist_str_vcvs(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_CCVS:
#                return self.get_netlist_str_ccvs(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_VCCS:
#                return self.get_netlist_str_vccs(flatten_inst_name, flatten_inst_node_names, inst)
#            case netlist.Type.INST_CCCS:
#                return self.get_netlist_str_cccs(flatten_inst_name, flatten_inst_node_names, inst)
#            case _:
#                return self.get_netlist_str_other(flatten_inst_name, flatten_inst_node_names, inst)
#
#    # rname n1 n2           value ...
#    # rname n1 n2 model r = value ...
#    def get_netlist_str_r(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{flatten_inst_name}"
#        #
#        for node in flatten_inst_node_names:
#            netlist_str += f" {node}"
#        #
#        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_r()]
#        #
#        if netlist.get_k_default_cellname_r() != inst.get_cell().get_name():
#            netlist_str += f" {self.get_cell().get_name()} r ="
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        for parameter_name in inst.get_equation_value_dic():
#            if netlist.get_k_default_cellname_r() == inst.get_cell().get_name():
#                continue
#            equation_value = inst.get_equation_value_dic()[parameter_name]
#            netlist_str += f" {parameter_name} = '{equation_value.get_equation()}'"
#        return netlist_str
#
#    # lname n1 n2 value
#    def get_netlist_str_l(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic[netlist.get_k_default_cellname_l()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # cname n1 n2 value
#    def get_netlist_str_c(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{flatten_inst_name}"
#        #
#        for nodename in flatten_inst_node_names:
#            netlist_str += f" {nodename}"
#        #
#        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_c()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # kname inductor1 inductor2 value
#    def get_netlist_str_k(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{flatten_inst_name}"
#        #
#        for nodename in flatten_inst_node_names:
#            netlist_str += f" {nodename}"
#        #
#        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_k()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # vname node1 node2 value
#    def get_netlist_str_vs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic["dc"]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # iname node1 node2 value
#    def get_netlist_str_cs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic["dc"]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # ename n1 n2 nc1 nc2 value
#    def get_netlist_str_vcvs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic[get_k_default_cellname_vcvs()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # gname n1 n2 nc1 nc2 value
#    def get_netlist_str_ccvs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic[get_k_default_cellname_ccvs()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # hname n1 n2 vcontrol value
#    def get_netlist_str_vccs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic[get_k_default_cellname_vccs()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # fname n1 n2 vcontrol value
#    def get_netlist_str_cccs(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{self.get_name()}"
#        # print(f"#debug- {self.get_name()} {self.m_equation_value_dic.keys()}")
#        #
#        for node in self.m_nodes:
#            netlist_str += f" {node.get_name()}"
#        #
#        equation_value = self.m_equation_value_dic[get_k_default_cellname_cccs()]
#        #
#        netlist_str += f" {equation_value.get_equation()}"
#        #
#        return netlist_str
#
#    # xname n1 n2 ... cell ...
#    def get_netlist_str_other(self, flatten_inst_name, flatten_inst_node_names, inst):
#        # inst_name
#        netlist_str = f"{flatten_inst_name}"
#        #
#        for nodename in flatten_inst_node_names:
#            netlist_str += f" {nodename}"
#        #
#        netlist_str += f" {inst.get_cell().get_name()}"
#        #
#        for parameter_name in inst.get_equation_value_dic():
#            equation_value = inst.get_equation_value_dic()[parameter_name]
#            netlist_str += f" {parameter_name} = '{equation_value.get_equation()}'"
#        #
#        return netlist_str
#
