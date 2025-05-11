import sys
import os
import inspect
import datetime
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import log
import netlist
import version
import run


class Write(run.Run):
    def __init__(self, t_input=None, t_netlist=None, add_first_char=False):
        super().__init__(t_input, t_netlist)
        self.__file_name = ""
        self.__add_first_char = add_first_char

    def set_file_name(self, filename):
        self.__file_name = filename

    def get_file_name(self):
        return self.__file_name

    def set_add_first_char(self, add_first_char):
        self.__add_first_char = add_first_char

    def get_add_first_char(self):
        return self.__add_first_char

    def write_header(self, file):
        file.write(f"*\n")
        file.write(f"{self.get_input().get_system_str("* ")}\n")
        file.write(f"*\n")

    def write_global_net(self, file):
        if 0 < len(self.get_netlist().get_global_net_names()):
            for net_name in self.get_netlist().get_global_net_names():
                file.write(f".global {net_name}\n")
        file.write(f"\n")

    def write_netlist_cells(self, file):
        cell_key = netlist.get_cell_key(netlist.k_DEFAULT_TOP_CELL_NAME(), netlist.Type.CELL_CELL)
        default_top_cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        #
        for t_cell_key in self.get_netlist().get_cell_dic():
            t_cell = self.get_netlist().get_cell_by_cell_key(t_cell_key)
            if None == t_cell:
                continue
            if t_cell.get_name() == netlist.k_DEFAULT_TOP_CELL_NAME():
                continue
            if True == netlist.is_default_cell(t_cell.get_name(), t_cell.get_type()):
                continue
            #
            if "*" == netlist.get_model_cell_name(t_cell.get_type()):
                self.write_netlist_cell(file, t_cell, True)
            else:
                self.write_netlist_model(file, t_cell)
        #
        self.write_netlist_cell(file, default_top_cell, False)

    def write_netlist_cell(self, file, cell, subckt=False):
        #
        if True == subckt:
            cell_line = f".subckt {cell.get_name()}"
            for pin in cell.get_pins():
                cell_line += f" {pin.get_name()}"
            netlist.write_wrap_line(file, cell_line)
            file.write("\n")
        #
        for t_cell_key in cell.get_cell_dic():
            t_cell = cell.get_cell_dic()[t_cell_key]
            if True == netlist.is_default_cell(t_cell.get_name(), t_cell.get_type()):
                continue
            #
            if "*" == netlist.get_model_cell_name(t_cell.get_type()):
                self.write_netlist_cell(file, t_cell, True)
            else:
                self.write_netlist_model(file, t_cell)
        #
        for inst_name in cell.get_inst_dic():
            node_names = []
            inst = cell.get_inst_dic()[inst_name]
            for node in inst.get_nodes():
                node_names.append(node.get_name())
            #
            inst_line = self.get_inst_line(inst_name, node_names, inst)
            netlist.write_wrap_line(file, inst_line)
            file.write("\n")
        #
        if True == subckt:
            file.write(".ends\n")
        file.write("\n")

    def write_netlist_model(self, file, cell):
        model_line = f".model"
        model_line += f" {cell.get_name()}"
        model_line += f" {netlist.get_model_cell_name(cell.get_type())}"
        for variable_name in cell.get_param().get_variable_names():
            equation = cell.get_param().get_equation_dic()[variable_name]
            model_line += f"  {variable_name}='{equation.get_s()}"
        netlist.write_wrap_line(file, model_line)
        file.write(f"\n\n")

    def get_instname_instnodes_line(self, inst_name, node_names, inst):
        s1 = f""
        if True == self.get_add_first_char():
            s1 += f"{netlist.get_first_char_inst(inst.get_type())}"
        else:
            s1 += f"{inst_name}"
        for node_name in node_names:
            s1 += f" {node_name}"
        return s1

    def get_inst_line(self, inst_name, node_names, inst):
        # print(f"# debug+++: yyy {inst.get_type()}")
        if None == inst:
            return f"* error: inst is None"
        #
        if (
            (netlist.Type.INST_R == inst.get_type())
            or (netlist.Type.INST_C == inst.get_type())
            or (netlist.Type.INST_L == inst.get_type())
        ):
            return self.get_inst_line_rlc(inst_name, node_names, inst)
        elif netlist.Type.INST_K == inst.get_type():
            return self.get_inst_line_k(inst_name, node_names, inst)
        elif (netlist.Type.INST_VS == inst.get_type()) or (netlist.Type.INST_CS == inst.get_type()):
            return self.get_inst_line_vs_cs(inst_name, node_names, inst)
        elif (netlist.Type.INST_VCVS == inst.get_type()) or (
            netlist.Type.INST_VCCS == inst.get_type()
        ):
            return self.get_inst_line_vcvs_vccs(inst_name, node_names, inst)
        elif (netlist.Type.INST_CCVS == inst.get_type()) or (
            netlist.Type.INST_CCCS == inst.get_type()
        ):
            return self.get_inst_line_ccvs_cccs(inst_name, node_names, inst)
        else:
            return self.get_inst_line_other(inst_name, node_names, inst)

    # rname n1 n2 value ...
    # rname n1 n2 model r=value ...
    def get_inst_line_rlc(self, inst_name, node_names, inst):
        # rname n1 n2
        inst_line = self.get_instname_instnodes_line(inst_name, node_names, inst)
        # r = value
        # value
        cell_name = inst.get_cell().get_name()
        # print(f"# debug+++: {cell_name}")
        if cell_name in ["r", "l", "c"]:
            if cell_name in inst.get_param().get_equation_dic():
                equation = inst.get_param().get_equation_dic()[cell_name]
            inst_line += f" '{equation.get_s()}'"
        else:
            inst_line += f" {cell_name}"
            for variable_name in ["r", "l", "c"]:
                if variable_name in inst.get_param().get_equation_dic():
                    equation = inst.get_param().get_equation_dic()[variable_name]
                    inst_line += f" {variable_name}='{equation.get_s()}'"
                    break
        # ...
        for variable_name in inst.get_param().get_variable_names():
            if variable_name in ["r", "l", "c"]:
                continue
            equation = inst.get_param().get_equation_dic()[variable_name]
            inst_line += f" {variable_name}='{equation.get_s()}'"
        return inst_line

    # kname inductor1 inductor2 value ...
    def get_inst_line_k(self, inst_name, node_names, inst):
        # kname
        inst_line = self.get_instname_instnodes_line(inst_name, node_names, inst)
        # l1 l2
        for inductor in inst.get_insts():
            inst_line += f" {inductor.get_name()}"
        # k = value
        # value
        cell_name = inst.get_cell().get_name()
        if cell_name in ["k"]:
            if cell_name in inst.get_param().get_equation_dic():
                equation = inst.get_param().get_equation_dic()[cell_name]
            inst_line += f" '{equation.get_s()}'"
        else:
            inst_line += f" {cell_name} {cell_name}="
            if cell_name in inst.get_param().get_equation_dic():
                equation = inst.get_param().get_equation_dic()[cell_name]
                inst_line += f"'{equation.get_s()}'"
        # ...
        for variable_name in inst.get_param().get_variable_names():
            if "k" == variable_name:
                continue
            equation = inst.get_param().get_equation_dic()[variable_name]
            inst_line += f" {variable_name}='{equation.get_s()}'"
        return inst_line

    # vname node1 node2 value
    # iname node1 node2 value
    def get_inst_line_vs_cs(self, inst_name, node_names, inst):
        #
        inst_line = self.get_instname_instnodes_line(inst_name, node_names, inst)
        #
        if "dc" in inst.get_param().get_equation_dic():
            equation = inst.get_param().get_equation_dic()["dc"]
            inst_line += f" {equation.get_s()}"
        else:
            inst_line += f" unknown"
        #
        return inst_line

    # ename n1 n2 nc1 nc2 value
    # gname n1 n2 nc1 nc2 value
    def get_inst_line_vcvs_vccs(self, instname, nodenames, inst):
        # ename n1 n2 nc1 nc2
        # gname n1 n2 nc1 nc2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # value
        cell_name = inst.get_cell().get_name()
        if cell_name in ["e", "g"]:
            equation = inst.get_param().get_equation_dic()[cell_name]
            inst_line += f" '{equation.get_s()}'"
        return inst_line

    # hname n1 n2 vcontrol value
    # fname n1 n2 vcontrol value ...
    def get_inst_line_ccvs_cccs(self, instname, nodenames, inst):
        # print(f"# debug+++: {inst.get_info_str()}")
        # fname n1 n2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # vcontrol
        for vcontrol in inst.get_insts():
            inst_line += f" {vcontrol.get_name()}"
        # value
        cell_name = inst.get_cell().get_name()
        if cell_name in ["h", "f"]:
            equation = inst.get_param().get_equation_dic()[cell_name]
            inst_line += f" '{equation.get_s()}'"
        return inst_line

    # xname n1 n2 ... cell ...
    # mname n1 n2 n3 n4 cell ...
    # dname n1 n2 cell ...
    # qname n1 n2 n3 cell ...
    def get_inst_line_other(self, inst_name, node_names, inst):
        # print(f"# debug+++: {inst.get_info_str()}")
        # xname n1 n2 ... nN
        inst_line = self.get_instname_instnodes_line(inst_name, node_names, inst)
        # cell
        inst_line += f" {inst.get_cell().get_name()}"
        # ...
        for variable_name in inst.get_param().get_variable_names():
            equation = inst.get_param().get_equation_dic()[variable_name]
            inst_line += f" {variable_name}='{equation.get_s()}'"
        return inst_line

    def run(self):
        file = open(self.__file_name, "wt")
        self.write_header(file)
        self.write_global_net(file)
        self.write_netlist_cells(file)
        file.close()
