import sys
import os
import inspect
import datetime
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import spiceutil.input.input as input
import spiceutil.log.log as log
import netlist
import spiceutil.version.version as version


class Write:
    def __init__(self, t_input=None, t_netlist=None, textwidth=100, add_first_char=False):
        self.__input = t_input
        self.__netlist = t_netlist
        self.__filename = ""
        self.__textwidth = textwidth
        self.__add_first_char = add_first_char

    def set_input(self, input):
        self.__input = input

    def get_input(self):
        return self.__input

    def set_filename(self, filename):
        self.__filename = filename

    def get_filename(self):
        return self.__filename

    def set_textwidth(self, textwidth):
        self.__textwidth = textwidth

    def get_textwidth(self):
        return self.__textwidth

    def set_add_first_char(self, add_first_char):
        self.__add_first_char = add_first_char

    def get_add_first_char(self):
        return self.__add_first_char

    def run(self):
        file = open(self.__filename, "wt")
        self.write_header(file)
        self.write_global_net(file)
        self.write_netlist(file)
        file.close()

    def write_header(self, file):
        file.write(f"*\n")
        file.write(f"{self.get_input().get_system_str("* ")}\n")
        file.write(f"*\n")

    def write_global_net(self, file):
        if 0 < len(self.get_netlist().get_global_netnames()):
            for netname in self.get_netlist().get_global_netnames():
                file.write(f".global {netname}\n")
        file.write(f"\n")

    def write_netlist(self, file):
        default_top_cell = self.get_netlist().get_cell(
            netlist.get_k_default_top_cellname(), netlist.Type.CELL_CELL
        )
        for key in self.get_netlist().get_cell_dic():
            cell = self.get_netlist().get_cell_by_key(key)
            if cell.get_name() in netlist.get_k_default_cellname_set():
                continue
            if netlist.get_k_default_top_cellname() == cell.get_name():
                continue
            self.write_netlist_cell(file, cell, True)
        if None != default_top_cell:
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
        for instname in cell.get_inst_dic():
            nodenames = []
            inst = cell.get_inst_dic()[instname]
            for node in inst.get_nodes():
                nodenames.append(node.get_name())
            #
            inst_line = self.get_inst_line(instname, nodenames, inst)
            netlist.write_wrap_line(file, inst_line)
            file.write("\n")
        #
        if True == subckt:
            file.write(".ends\n")
        file.write("\n")

    def get_instname_instnodes_line(self, instname, nodenames, inst):
        s1 = f""
        if True == self.get_add_first_char():
            s1 += f"{netlist.get_first_char_inst(inst.get_type())}"
        else:
            s1 += f"{instname}"
        for nodename in nodenames:
            s1 += f" {nodename}"
        return s1

    def get_inst_line(self, instname, nodenames, inst):
        # print(f"{instname} {nodenames}")
        match inst.get_type():
            case netlist.Type.INST_R:
                return self.get_inst_line_r(instname, nodenames, inst)
            case netlist.Type.INST_L:
                return self.get_inst_line_l(instname, nodenames, inst)
            case netlist.Type.INST_C:
                return self.get_inst_line_c(instname, nodenames, inst)
            case netlist.Type.INST_K:
                return self.get_inst_line_k(instname, nodenames, inst)
            case netlist.Type.INST_VS:
                return self.get_inst_line_vs(instname, nodenames, inst)
            case netlist.Type.INST_CS:
                return self.get_inst_line_cs(instname, nodenames, inst)
            case netlist.Type.INST_VCVS:
                return self.get_inst_line_vcvs(instname, nodenames, inst)
            case netlist.Type.INST_CCVS:
                return self.get_inst_line_ccvs(instname, nodenames, inst)
            case netlist.Type.INST_VCCS:
                return self.get_inst_line_vccs(instname, nodenames, inst)
            case netlist.Type.INST_CCCS:
                return self.get_inst_line_cccs(instname, nodenames, inst)
            case _:
                return self.get_inst_line_other(instname, nodenames, inst)

    # rname n1 n2 value ...
    # rname n1 n2 model r=value ...
    def get_inst_line_r(self, instname, nodenames, inst):
        # rname n1 n2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # r = value
        # value
        if netlist.get_k_default_cellname_r() != inst.get_cell().get_name():
            inst_line += f" {inst.get_cell().get_name()} r="
        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_r()]
        inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_r() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # lname n1 n2 value ...
    # lname n1 n2 mode l=value ...
    def get_inst_line_l(self, instname, nodenames, inst):
        # lname n1 n2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # l = value
        # value
        if netlist.get_k_default_cellname_l() != inst.get_cell().get_name():
            inst_line += f" {inst.get_cell().get_name()} l="
        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_l()]
        inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_l() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # cname n1 n2 value ...
    # cname n1 n2 model c=value ...
    def get_inst_line_c(self, instname, nodenames, inst):
        # cname n1 n2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # c = value
        # value
        if netlist.get_k_default_cellname_c() != inst.get_cell().get_name():
            inst_line += f" {inst.get_cell().get_name()} c="
        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_c()]
        inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_c() == param_name:
                continue
            equation_value = self.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # kname inductor1 inductor2 value ...
    def get_inst_line_k(self, instname, nodenames, inst):
        # kname
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # l1 l2
        for inductor in inst.get_insts():
            inst_line += f" {inductor.get_name()}"
        # k = value
        # value
        if netlist.get_k_default_cellname_k() != inst.get_cell().get_name():
            inst_line += f" {inst.get_cell().get_name()} k="
        equation_value = inst.get_equation_value_dic()[netlist.get_k_default_cellname_k()]
        inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_k() == param_name:
                continue
            equation_value = self.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # vname node1 node2 value ...
    def get_inst_line_vs(self, instname, nodenames, inst):
        #
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        #
        if "dc" in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()["dc"]
            inst_line += f" {equation_value.get_equation()}"
        else:
            for param_name in inst.get_param_names():
                equation_value = self.get_equation_value_dic()[param_name]
                inst_line += f" {param_name}='{equation_value.get_equation()}'"
        #
        return inst_line

    # iname node1 node2 value ...
    def get_inst_line_cs(self, instname, nodenames, inst):
        #
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        #
        if "dc" in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()["dc"]
            inst_line += f" {equation_value.get_equation()}"
        else:
            for param_name in inst.get_param_names():
                equation_value = inst.get_equation_value_dic()[param_name]
                inst_line += f" {param_name} = '{equation_value.get_equation()}'"
        #
        return inst_line

    # ename n1 n2 nc1 nc2 value
    def get_inst_line_vcvs(self, instname, nodenames, inst):
        # ename n1 n2 nc1 nc2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # value
        if netlist.get_k_default_cellname_vcvs() in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()[
                netlist.get_k_default_cellname_vcvs()
            ]
            inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_vcvs() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # gname n1 n2 nc1 nc2 value
    def get_inst_line_ccvs(self, instname, nodenames, inst):
        # ename n1 n2 nc1 nc2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # value
        if netlist.get_k_default_cellname_ccvs() in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()[
                netlist.get_k_default_cellname_ccvs()
            ]
            inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_ccvs() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # hname n1 n2 vcontrol value
    def get_inst_line_vccs(self, instname, nodenames, inst):
        # ename n1 n2 nc1 nc2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # value
        if netlist.get_k_default_cellname_vccs() in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()[
                netlist.get_k_default_cellname_vccs()
            ]
            inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_vccs() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # fname n1 n2 vcontrol value ...
    def get_inst_line_cccs(self, instname, nodenames, inst):
        # fname n1 n2
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # vcontrol
        for vcontrol in inst.get_insts():
            inst_line += f" {vcontrol.get_name()}"
        # value
        if netlist.get_k_default_cellname_cccs() in inst.get_equation_value_dic():
            equation_value = inst.get_equation_value_dic()[
                netlist.get_k_default_cellname_cccs()
            ]
            inst_line += f" '{equation_value.get_equation()}'"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_cccs() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line

    # xname n1 n2 ... cell ...
    # mname n1 n2 n3 n4 cell ...
    # dname n1 n2 cell ...
    # qname n1 n2 n3 cell ...
    def get_inst_line_other(self, instname, nodenames, inst):
        # xname n1 n2 ... nN
        inst_line = self.get_instname_instnodes_line(instname, nodenames, inst)
        # cell
        inst_line += f" {inst.get_cell().get_name()}"
        # ...
        for param_name in inst.get_param_names():
            if netlist.get_k_default_cellname_c() == param_name:
                continue
            equation_value = inst.get_equation_value_dic()[param_name]
            inst_line += f" {param_name}='{equation_value.get_equation()}'"
        return inst_line


#    def get_netlist_str(self):
#        netlist_str = []
#        #
#        for key in self.m_cell_dic:
#            cell = self.m_cell_dic[key]
#            if get_k_default_top_cellname() == cell.get_name():
#                continue
#            netlist_str += cell.get_netlist_str()
#        #
#        k_top_cell_key = self.get_cell_key(get_k_default_top_cellname(), Type.CELL_CELL)
#        if k_top_cell_key in self.m_cell_dic:
#            cell = self.m_cell_dic[k_top_cell_key]
#            netlist_str += cell.get_netlist_str(False)
#        #
#        return netlist_str
#
#    def write_netlist(self, logger=None, filename=None, width=120, header=""):
#        if None == logger:
#            if None == filename:
#                print(f"# write netlist start ... {datetime.datetime.now()}")
#                for netlist_line in self.get_netlist_str():
#                    wrap_netlist_lines = textwrap.wrap(
#                        netlist_line,
#                        width=width,
#                        subsequent_indent="+ ",
#                        break_long_words=False,
#                        break_on_hyphens=False,
#                    )
#                    for wrap_netlist_line in wrap_netlist_lines:
#                        print(f"{wrap_netlist_line}")
#                print(f"# write netlist end ... {datetime.datetime.now()}\n")
#            else:
#                print(f"# write netlist start ... {datetime.datetime.now()}")
#                print(f"netlist file : {filename}")
#                f = open(filename, "wt")
#                f.write(f"* {header}\n")
#                for netlist_line in self.get_netlist_str():
#                    wrap_netlist_lines = textwrap.wrap(
#                        netlist_line,
#                        width=width,
#                        subsequent_indent="+ ",
#                        break_long_words=False,
#                        break_on_hyphens=False,
#                    )
#                    for wrap_netlist_line in wrap_netlist_lines:
#                        f.write(f"{wrap_netlist_line}\n")
#                f.close()
#                print(f"# write netlist end ... {datetime.datetime.now()}\n")
#        else:
#            if None == filename:
#                logger.info(f"# write netlist start ... {datetime.datetime.now()}")
#                for netlist_line in self.get_netlist_str():
#                    wrap_netlist_lines = textwrap.wrap(
#                        netlist_line,
#                        width=width,
#                        subsequent_indent="+ ",
#                        break_long_words=False,
#                        break_on_hyphens=False,
#                    )
#                    for wrap_netlist_line in wrap_netlist_lines:
#                        logger.info(f"{wrap_netlist_line}")
#                logger.info(f"# write netlist end ... {datetime.datetime.now()}\n")
#            else:
#                logger.info(f"# write netlist start ... {datetime.datetime.now()}")
#                logger.info(f"netlist file : {filename}")
#                f = open(filename, "wt")
#                f.write(f"* {header}\n")
#                for netlist_line in self.get_netlist_str():
#                    wrap_netlist_lines = textwrap.wrap(
#                        netlist_line,
#                        width=width,
#                        subsequent_indent="+ ",
#                        break_long_words=False,
#                        break_on_hyphens=False,
#                    )
#                    for wrap_netlist_line in wrap_netlist_lines:
#                        f.write(f"{wrap_netlist_line}\n")
#                f.close()
#                logger.info(f"# write netlist end ... {datetime.datetime.now()}\n")
#
#
#
