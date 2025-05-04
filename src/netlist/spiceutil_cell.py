from .spiceutil_object import Object
from .spiceutil_param import Param
from .spiceutil_inst import Inst
from .spiceutil_utils import *


class Cell(Object):
    def __init__(self, name="", type=Type.INIT):
        super().__init__(name, type)
        self.__node_dic = {}  # key : name, data : inst
        self.__inst_dic = {}  # key : name, data : node
        self.__cell_dic = {}  # key : name, data : cell(model)
        self.__pins = []
        self.__pin_set = set(self.__pins)
        self.__inst_names = []
        self.__node_names = []
        self.__param = Param()
        self.__inst_count = 0

    def get_inst_dic(self):
        return self.__inst_dic

    def get_node_dic(self):
        return self.__node_dic

    def get_cell_dic(self):
        return self.__cell_dic

    def get_pins(self):
        return self.__pins

    def get_pin_set(self):
        return self.__pin_set

    def make_pin_set(self):
        self.__pin_set = set(self.__pins)

    def get_pin(self, pos):
        if pos < len(self.get_pins()):
            return self.__pins(pos)
        else:
            return None

    def get_inst_names(self):
        return self.__inst_names

    def get_node_names(self):
        return self.__node_names

    def get_node(self, name):
        if name in self.__node_dic:
            return self.__node_dic[name]
        else:
            return None

    def get_inst(self, name):
        if name in self.__inst_dic:
            return self.__inst_dic[name]
        else:
            return None

    def get_cell(self, name):
        if name in self.__cell_dic:
            return self.__cell_dic[name]
        else:
            return None

    def add_node(self, node):
        if not node.get_name() in self.__node_dic:
            self.__node_dic[node.get_name()] = node

    def add_inst(self, inst):
        if not inst.get_name() in self.__inst_dic:
            self.__inst_dic[inst.get_name()] = inst

    def add_cell(self, cell):
        if not cell.get_name() in self.__cell_dic:
            self.__cell_dic[cell.get_name()] = cell

    def add_pin(self, pin):
        self.__pins.append(pin)

    def increase_inst_count(self, inst_count_step=1):
        self.__inst_count += inst_count_step

    def set_inst_count(self, inst_count):
        self.__inst_count = inst_count

    def get_inst_count(self):
        return self.__inst_count

    def set_param(self, param):
        self.__param = param

    def get_param(self):
        return self.__param
