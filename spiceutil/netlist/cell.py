import os
import sys

from .inst import Inst
from .node import Node
from .object import Object
from .parameters import Parameters

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


class Cell(Object, Parameters):
    def __init__(self, name="", type=utils.Type.INIT, selected=False):
        super().__init__(name, type, selected)
        self.__inst_dic = {}  # key : name, data : Inst
        self.__node_dic = {}  # key : name, data : Node
        self.__model_dic = {}  # key : name, data : Cell(model)
        self.__pins = []
        self.__pin_set = None

    def get_inst_dic(self):
        return self.__inst_dic

    def add_inst(self, name, inst):
        if not name in self.__inst_dic:
            self.__inst_dic[name] = inst

    def get_inst(self, name):
        if name in self.__inst_dic:
            return self.__inst_dic[name]
        else:
            return None

    def get_node_dic(self):
        return self.__node_dic

    def add_node(self, name, node):
        if not name in self.__node_dic:
            self.__node_dic[name] = node

    def get_node(self, name):
        if name in self.__node_dic:
            return self.__node_dic[name]
        else:
            return None

    def get_model_dic(self):
        return self.__model_dic

    def add_model(self, name, model):
        if not name in self.__model_dic:
            self.__model_dic[name] = model

    def get_model(self, name):
        if name in self.__model_dic:
            return self.__model_dic[name]
        else:
            return None

    def get_pins(self):
        return self.__pins

    def add_pin(self, name, pin):
        if not name in self.__node_dic:
            self.__node_dic[name] = pin
            self.__pins.append(pin)

    def make_pin_set(self):
        self.__pin_set = set(self.__pins)

    def get_netlist_str(self, write_subckt_ends=True):
        match self.get_type():
            case utils.Type.CELL_CELL:
                return self.get_netlist_str_cell(write_subckt_ends)
            case utils.Type.CELL_NMOS:
                return self.get_netlist_str_model()
            case utils.Type.CELL_PMOS:
                return self.get_netlist_str_model()
            case utils.Type.CELL_NPN:
                return self.get_netlist_str_model()
            case utils.Type.CELL_PNP:
                return self.get_netlist_str_model()
            case utils.Type.CELL_NJF:
                return self.get_netlist_str_model()
            case utils.Type.CELL_PJF:
                return self.get_netlist_str_model()
            case _:
                return ""

    def get_netlist_str_cell(self, write_subckt_ends=True):
        netlist_str = []
        if True == write_subckt_ends:
            netlist_str_subckt = f".subckt {self.get_name()}"
            for pin in self.get_pins():
                netlist_str_subckt += f" {pin.get_name()}"
            for parameter_name in self.m_equation_value_dic:
                equation_values = self.m_equation_value_dic[parameter_name]
                netlist_str_subckt += f" {parameter_name} = '{
                    equation_values.get_equation()}'"
            netlist_str.append(netlist_str_subckt)
        for inst_name in self.__inst_dic:
            inst = self.__inst_dic[inst_name]
            netlist_str.append(inst.get_netlist_str())
        if True == write_subckt_ends:
            netlist_str.append(f".ends")
        return netlist_str

    def get_netlist_str_model(self):
        netlist_str = []
        netlist_str_model = f".model {
            self.get_name()} {utils.Utils().get_type_name(self.get_type())}"
        for parameter_name in self.m_equation_value_dic:
            equation_value = self.m_equation_value_dic[parameter_name]
            netlist_str_model += f" {parameter_name} = {
                equation_value.get_equation()}"
        netlist_str.append(netlist_str_model)
        return netlist_str

    def get_inst_info_str(self):
        info_str = f"\n{self.get_name()} #pin : {len(self.get_pins())}"
        for inst_name in self.get_inst_dic():
            inst = self.get_inst_dic()[inst_name]
            cell = inst.get_cell()
            # if None == cell:
            #    print(f"#debug- {inst_name}")
            info_str += f"\n{inst_name} {cell.get_name()} {cell.get_type()}"
        return info_str
