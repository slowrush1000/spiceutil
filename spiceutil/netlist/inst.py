import os
import sys

from .object import Object
from .node import Node
from .parameters import Parameters

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


class Inst(Object, Parameters):
    def __init__(self, name="", type=utils.Type.INIT, selected=False):
        super().__init__(name, type, selected)
        self.__nodes = []
        self.__insts = []
        self.__cell = None

    def get_nodes(self):
        return self.__nodes

    def add_node(self, node):
        self.__nodes.append(node)

    def get_node(self, pos):
        if pos < len(self.__nodes):
            return self.__nodes[pos]
        else:
            return None

    def get_insts(self):
        return self.__insts

    def add_inst(self, inductor):
        self.__insts.append(inductor)

    def get_inst(self, pos):
        if pos < len(self.__insts):
            return self.__insts[pos]
        else:
            return None

    def set_cell(self, cell):
        self.__cell = cell

    def get_cell(self):
        return self.__cell
