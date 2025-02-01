#
from .spiceutil_object import Object
from .spiceutil_parameters import Parameters
from .spiceutil_inst import Inst
from .spiceutil_utils import *


class Cell(Object, Parameters):
    def __init__(self, name="", type=Type.INIT):
        super().__init__()
        self.m_name = name
        self.m_type = type
        self.m_inst_dic = {}  # key : name, data : inst
        self.m_node_dic = {}  # key : name, data : node
        self.m_pins = []
        self.m_pin_set = None
        self.m_inst_size = 0

    def is_exist_inst(self, name):
        if name in self.m_inst_dic:
            return True
        else:
            return False

    def add_inst(self, name, inst):
        if not name in self.m_inst_dic:
            self.m_inst_dic[name] = inst

    def get_inst(self, name):
        if True == self.is_exist_inst(name):
            return self.m_inst_dic[name]
        else:
            return None

    def get_inst_dic(self):
        return self.m_inst_dic

    def is_exist_node(self, name):
        if name in self.m_node_dic:
            return True
        else:
            return False

    def add_node(self, name, node):
        if not name in self.m_node_dic:
            self.m_node_dic[name] = node

    def get_node(self, name):
        if True == self.is_exist_node(name):
            return self.m_node_dic[name]
        else:
            return None

    def get_node_dic(self):
        return self.m_node_dic

    def add_pin(self, name, pin):
        if not name in self.m_node_dic:
            self.m_node_dic[name] = pin
            self.m_pins.append(pin)

    def make_pin_set(self):
        self.m_pin_set = set(self.m_pins)

    def get_pins(self):
        return self.m_pins

    def SetInstSize(self, inst_size):
        self.m_inst_size = inst_size

    def get_inst_size(self):
        return self.m_inst_size

    def increase_inst_size(self, increase_size=1):
        self.m_inst_size += increase_size

    def get_netlist_str(self, write_subckt_ends=True):
        match self.get_type():
            case Type.CELL_CELL:
                return self.get_netlist_str_cell(write_subckt_ends)
            case Type.CELL_NMOS:
                return self.get_netlist_str_model()
            case Type.CELL_PMOS:
                return self.get_netlist_str_model()
            case Type.CELL_NPN:
                return self.get_netlist_str_model()
            case Type.CELL_PNP:
                return self.get_netlist_str_model()
            case Type.CELL_NJF:
                return self.get_netlist_str_model()
            case Type.CELL_PJF:
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
        for inst_name in self.m_inst_dic:
            inst = self.m_inst_dic[inst_name]
            netlist_str.append(inst.get_netlist_str())
        if True == write_subckt_ends:
            netlist_str.append(f".ends")
        return netlist_str

    def get_netlist_str_model(self):
        netlist_str = []
        netlist_str_model = f".model {
            self.get_name()} {get_type_name(self.get_type())}"
        for parameter_name in self.m_equation_value_dic:
            equation_value = self.m_equation_value_dic[parameter_name]
            netlist_str_model += f" {parameter_name} = {
                equation_value.get_equation()}"
        netlist_str.append(netlist_str_model)
        return netlist_str

    def get_inst_info_str(self):
        info_str = f"{self.get_name()} #pin : {len(self.get_pins())}\n"
        for inst_name in self.get_inst_dic():
            inst = self.get_inst_dic()[inst_name]
            cell = inst.get_cell()
            info_str += f"{inst_name} {cell.get_name()} {cell.get_type()}\n"
        return info_str
