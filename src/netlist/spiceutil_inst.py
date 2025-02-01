from .spiceutil_object import Object
from .spiceutil_parameters import Parameters
from .spiceutil_utils import *


class Inst(Object, Parameters):
    def __init__(self, name="", type=Type.INIT):
        super().__init__()
        self.m_name = name
        self.m_type = type
        self.m_nodes = []
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

    def set_cell(self, cell):
        self.m_cell = cell

    def get_cell(self):
        return self.m_cell

    def get_netlist_str(self):
        # print(f'debug- {self.get_name()} {self.get_cell().get_name()}')
        for parameter_name_1 in self.m_equation_value_dic:
            equation_value_1 = self.m_equation_value_dic[parameter_name_1]
            # print(f'debug- {parameter_name_1} : {equation_value_1.get_equation()}')
        #
        netlist_str = f"{self.get_name()}"
        for node in self.m_nodes:
            netlist_str += f" {node.get_name()}"
        #
        if (k_DEFAULT_R_CELL == self.get_cell().get_name()) and (
            Type.INST_R == self.set_type()
        ):
            if k_DEFAULT_R_CELL in self.m_equation_value_dic:
                equation_value = self.m_equation_value_dic[get_default_r_cell()]
                netlist_str += f" {equation_value.get_equation()}"
        elif (k_DEFAULT_L_CELL == self.get_cell().get_name()) and (
            Type.INST_L == self.set_type()
        ):
            if k_DEFAULT_L_CELL in self.m_equation_value_dic:
                equation_value = self.m_equation_value_dic[k_DEFAULT_L_CELL()]
                netlist_str += f" {equation_value.get_equation()}"
        elif (k_DEFAULT_C_CELL == self.get_cell().get_name()) and (
            Type.INST_C == self.set_type()
        ):
            if k_DEFAULT_C_CELL in self.m_equation_value_dic:
                equation_value = self.m_equation_value_dic[get_default_c_cell()]
                netlist_str += f" {equation_value.get_equation()}"
        else:
            netlist_str += f" {self.get_cell().get_name()}"
        #
        for parameter_name in self.m_equation_value_dic:
            if (
                (k_DEFAULT_R_CELL == self.get_cell().get_name())
                or (k_DEFAULT_L_CELL == self.get_cell().get_name())
                or (k_DEFAULT_C_CELL == self.get_cell().get_name())
            ):
                continue
            equation_value = self.m_equation_value_dic[parameter_name]
            netlist_str += f" {parameter_name} = '{equation_value.get_equation()}'"
        return netlist_str
        #
