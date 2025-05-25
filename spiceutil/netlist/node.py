import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from netlist.object import Object
import utils


class Node(Object):
    def __init__(self, name="", type=utils.Type_tt.INIT, selected=False):
        super().__init__(name, type, selected)
        self.__insts = []

    def get_insts(self):
        return self.__insts

    def add_inst(self, inst):
        self.__insts.append(inst)

    def get_inst(self, pos):
        if pos < len(self.__insts):
            return self.__insts[pos]
        else:
            return None
