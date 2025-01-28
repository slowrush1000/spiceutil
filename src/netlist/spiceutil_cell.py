#
from .spiceutil_object      import Object
from .spiceutil_parameters  import Parameters
from .spiceutil_utils       import Type
from .spiceutil_utils       import GetTypeName
#
class Cell(Object, Parameters):
    def __init__(self, name = '', type = Type.INIT):
        super().__init__()
        self.m_name     = name
        self.m_type     = type
        self.m_inst_dic = {}    # key : name, data : inst
        self.m_node_dic = {}    # key : name, data : node
        self.m_pins     = []
        self.m_pin_set  = None
    def IsExistInst(self, name):
        if name in self.m_inst_dic:
            return True
        else:
            return False
    def AddInst(self, name, inst):
        if not name in self.m_inst_dic:
            self.m_inst_dic[name]  = inst
    def GetInst(self, name):
        if True == self.IsExistInst(name):
            return self.m_inst_dic[name]
        else:
            return None
    def GetInstDic(self):
        return self.m_inst_dic
    def IsExistNode(self, name):
        if name in self.m_node_dic:
            return True
        else:
            return False
    def AddNode(self, name, node):
        if not name in self.m_node_dic:
            self.m_node_dic[name]  = node
    def GetNode(self, name):
        if True == self.IsExistNode(name):
            return self.m_node_dic[name]
        else:
            return None
    def GetNodeDic(self):
        return self.m_node_dic
    def AddPin(self, name, pin):
        if not name in self.m_node_dic:
            self.m_node_dic[name]  = pin
            self.m_pins.append(pin)
    def MakePinSet(self):
        self.m_pin_set  = set(self.m_pins)
    def GetPins(self):
        return self.m_pins
    def GetNetlistStr(self, write_subckt_ends = True):
        match self.GetType():
            case Type.CELL_CELL:
                return self.GetNetlistStrCell(write_subckt_ends)
            case Type.CELL_NMOS:
                return self.GetNetlistStrModel()
            case Type.CELL_PMOS:
                return self.GetNetlistStrModel()
            case Type.CELL_NPN:
                return self.GetNetlistStrModel()
            case Type.CELL_PNP:
                return self.GetNetlistStrModel()
            case Type.CELL_NJF:
                return self.GetNetlistStrModel()
            case Type.CELL_PJF:
                return self.GetNetlistStrModel()
            case _:
                return ''
    def GetNetlistStrCell(self, write_subckt_ends = True):
        netlist_str     = ''
        if True == write_subckt_ends:
            netlist_str     += f'.subckt {self.GetName()}'
            for pin in self.GetPins():
                netlist_str += f' {pin.GetName()}'
            for parameter_name in self.m_equation_value_dic:
                equation_values = self.m_equation_value_dic[parameter_name]
                netlist_str += f" {parameter_name} = '{equation_values.GetEquation()}'"
            netlist_str     += '\n'
        for inst_name in self.m_inst_dic:
            inst        = self.m_inst_dic[inst_name]
            netlist_str += inst.GetNetlistStr()
        if True == write_subckt_ends:
            netlist_str     += f'.ends'
        netlist_str     += f'\n'
        return netlist_str
    def GetNetlistStrModel(self):
        netlist_str     = ''
        netlist_str     += f'.model {self.GetName()} {GetTypeName(self.GetType())}'
        netlist_str     += f'\n'
        return netlist_str
