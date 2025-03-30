from .spiceutil_object import Object
from .spiceutil_parameters import Parameters
from .spiceutil_utils import *


class Inst(Object, Parameters):
    def __init__(self, name="", type=Type.INIT):
        super().__init__()
        self.m_name = name
        self.m_type = type
        self.m_nodes = []
        self.m_insts = []
        self.m_cell = None

    def add_node(self, node):
        self.m_nodes.append(node)

    def get_nodes(self):
        return self.m_nodes

    def get_node(self, pos):
        if pos < len(self.m_nodes):
            return self.m_nodes[pos]
        else:
            return None

    def get_node_size(self):
        return len(self.get_nodes())

    def add_inst(self, inductor):
        self.m_insts.append(inductor)

    def get_insts(self):
        return self.m_insts

    def get_inst(self, pos):
        if pos < len(self.m_insts):
            return self.m_insts[pos]
        else:
            return None

    def set_cell(self, cell):
        self.m_cell = cell

    def get_cell(self):
        return self.m_cell

    def get_netlist_str(self):
        # print(f'debug- {self.get_name()} {self.get_cell().get_name()}')
        # for parameter_name_1 in self.m_equation_value_dic:
        #    equation_value_1 = self.m_equation_value_dic[parameter_name_1]
        #    # print(f'debug- {parameter_name_1} : {equation_value_1.get_equation()}')
        #
        match self.get_type():
            case Type.INST_R:
                return self.get_netlist_str_r()
            case Type.INST_L:
                return self.get_netlist_str_l()
            case Type.INST_C:
                return self.get_netlist_str_c()
            case Type.INST_K:
                return self.get_netlist_str_k()
            case Type.INST_VS:
                return self.get_netlist_str_vs()
            case Type.INST_CS:
                return self.get_netlist_str_cs()
            case Type.INST_VCVS:
                return self.get_netlist_str_vcvs()
            case Type.INST_CCVS:
                return self.get_netlist_str_ccvs()
            case Type.INST_VCCS:
                return self.get_netlist_str_vccs()
            case Type.INST_CCCS:
                return self.get_netlist_str_cccs()
            case _:
                return self.get_netlist_str_other()

    #        netlist_str = f"{self.get_name()}"
    #        for node in self.m_nodes:
    #            netlist_str += f" {node.get_name()}"
    #        #
    #        if (get_k_default_cellname_r() == self.get_cell().get_name()) and (
    #            Type.INST_R == self.get_type()
    #        ):
    #            if get_k_default_cellname_r() in self.m_equation_value_dic:
    #                equation_value = self.m_equation_value_dic[
    #                    get_k_default_cellname_r()
    #                ]
    #                netlist_str += f" {equation_value.get_equation()}"
    #        elif (get_k_default_cellname_l() == self.get_cell().get_name()) and (
    #            Type.INST_L == self.get_type()
    #        ):
    #            if get_k_default_cellname_l() in self.m_equation_value_dic:
    #                equation_value = self.m_equation_value_dic[
    #                    get_k_default_cellname_l()
    #                ]
    #                netlist_str += f" {equation_value.get_equation()}"
    #        elif (get_k_default_cellname_c() == self.get_cell().get_name()) and (
    #            Type.INST_C == self.get_type()
    #        ):
    #            if get_k_default_cellname_c() in self.m_equation_value_dic:
    #                equation_value = self.m_equation_value_dic[
    #                    get_k_default_cellname_c()
    #                ]
    #                netlist_str += f" {equation_value.get_equation()}"
    #        else:
    #            netlist_str += f" {self.get_cell().get_name()}"
    #        #
    #        for parameter_name in self.m_equation_value_dic:
    #            if (
    #                (get_k_default_cellname_r() == self.get_cell().get_name())
    #                or (get_k_default_cellname_l() == self.get_cell().get_name())
    #                or (get_k_default_cellname_c() == self.get_cell().get_name())
    #            ):
    #                continue
    #            equation_value = self.m_equation_value_dic[parameter_name]
    #            netlist_str += (
    #                f" {parameter_name} = '{equation_value.get_equation()}'"
    #            )
    #        return netlist_str
    #

    # rname n1 n2           value ...
    # rname n1 n2 model r = value ...
    def get_netlist_str_r(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[get_k_default_cellname_r()]
        #
        if get_k_default_cellname_r() != self.get_cell().get_name():
            netlist_str += f" {self.get_cell().get_name()} r ="
        netlist_str += f" {equation_value.get_equation()}"
        #
        for parameter_name in self.m_equation_value_dic:
            if get_k_default_cellname_r() == self.get_cell().get_name():
                continue
            equation_value = self.m_equation_value_dic[parameter_name]
            netlist_str += (
                f" {parameter_name} = '{equation_value.get_equation()}'"
            )
        return netlist_str

    # lname n1 n2 value
    def get_netlist_str_l(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[get_k_default_cellname_l()]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # cname n1 n2 value
    def get_netlist_str_c(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[get_k_default_cellname_c()]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # kname inductor1 inductor2 value
    def get_netlist_str_k(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        for inductor in self.m_insts:
            netlist_str += f" {inductor.get_name()}"
        #
        equation_value = self.m_equation_value_dic[get_k_default_cellname_k()]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # vname node1 node2 value
    def get_netlist_str_vs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic["dc"]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # iname node1 node2 value
    def get_netlist_str_cs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic["dc"]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # ename n1 n2 nc1 nc2 value
    def get_netlist_str_vcvs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[
            get_k_default_cellname_vcvs()
        ]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # gname n1 n2 nc1 nc2 value
    def get_netlist_str_ccvs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[
            get_k_default_cellname_ccvs()
        ]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # hname n1 n2 vcontrol value
    def get_netlist_str_vccs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[
            get_k_default_cellname_vccs()
        ]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # fname n1 n2 vcontrol value
    def get_netlist_str_cccs(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        # print(f"#debug- {self.get_name()} {self.m_equation_value_dic.keys()}")
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        equation_value = self.m_equation_value_dic[
            get_k_default_cellname_cccs()
        ]
        #
        netlist_str += f" {equation_value.get_equation()}"
        #
        return netlist_str

    # xname n1 n2 ... cell ...
    def get_netlist_str_other(self):
        # inst_name
        netlist_str = f"{self.get_name()}"
        #
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        netlist_str += f" {self.get_cell().get_name()}"
        #
        for parameter_name in self.m_equation_value_dic:
            equation_value = self.m_equation_value_dic[parameter_name]
            netlist_str += (
                f" {parameter_name} = '{equation_value.get_equation()}'"
            )
        #
        return netlist_str
