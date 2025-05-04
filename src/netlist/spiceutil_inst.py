from .spiceutil_object import Object
from .spiceutil_param import Param
from .spiceutil_node import Node
from .spiceutil_utils import *


class Inst(Object):
    def __init__(self, name="", type=Type.INIT):
        super().__init__(name, type)
        self.__nodes = []
        self.__insts = []
        self.__cell = None
        self.__param = Param()

    def get_nodes(self):
        return self.__nodes

    def get_insts(self):
        return self.__insts

    def set_cell(self, cell):
        self.__cell = cell

    def get_cell(self):
        return self.__cell

    def add_node(self, node):
        self.__nodes.append(node)

    def add_inst(self, inst):
        self.__insts.append(inst)

    def set_param(self, param):
        self.__param = param

    def get_param(self):
        return self.__param

    def get_info_str(self):
        s1 = f"name: {self.get_name()}"
        s1 += f" node:"
        for node in self.get_nodes():
            s1 += f" {node.get_name()}"
        s1 += f" cell:"
        s1 += f" {self.get_cell().get_name()}"
        s1 += f" inst:"
        if 0 == len(self.get_insts()):
            s1 += f" *"
        else:
            for inst in self.get_insts():
                s1 += f" {inst.get_name()}"
        s1 += f" param:"
        for variable_name in self.get_param().get_variable_names():
            equation = self.get_param().get_equation_dic()[variable_name]
            s1 += f" {variable_name}='{equation.get_s()}'"
        return s1
