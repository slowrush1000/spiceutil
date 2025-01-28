#
from enum import Enum
import datetime
#
def k_TOP_CELLNAME():
    return '___xxx_top_xxx___'
def k_LINE_STEP():
    return 1_000_000
#
class Type(Enum):
    INIT            = 0
    #
    NODE_PIN        = 1
    NODE_NODE       = 2
    #
    CELL_R          = 10
    CELL_L          = 11
    CELL_C          = 12
    CELL_DIODE      = 14
    CELL_MOSFET     = 15
    CELL_BJT        = 16
    CELL_JFET       = 17
    CELL_CELL       = 18
    #
    CELL_NMOS       = 20
    CELL_PMOS       = 21
    CELL_NPN        = 22
    CELL_PNP        = 23
    CELL_NJF        = 24
    CELL_PJF        = 25
    #
    CELL_DIODE_S    = 30
    CELL_NMOS_S     = 31
    CELL_PMOS_S     = 32
    CELL_NPN_S      = 33
    CELL_PNP_S      = 34
    CELL_NJF_S      = 35
    CELL_PJF_S      = 36
    #
    INST_R          = 50
    INST_L          = 51
    INST_C          = 52
    INST_DIODE      = 53
    INST_MOSFET     = 54
    INST_BJT        = 55
    INST_JFET       = 56
    INST_INST       = 57
#
def GetTypeName(type):
    match type:
        case Type.CELL_R:
            return 'r'
        case Type.CELL_L:
            return 'l'
        case Type.CELL_C:
            return 'c'
        case Type.CELL_DIODE:
            return 'd'
        case Type.CELL_NMOS:
            return 'nmos'
        case Type.CELL_PMOS:
            return 'pmos'
        case Type.CELL_NPN:
            return 'npn'
        case Type.CELL_PNP:
            return 'pnp'
        case Type.CELL_NJF:
            return 'njf'
        case Type.CELL_PJF:
            return  'pjf'
        case _:
            return ''

class Run(Enum):
    MAKEIPROBE      =   0

class Object:
    def __init__(self, name = '', type = Type.INIT):
        super().__init__()
        self.m_name             = name
        self.m_type             = type
    def SetName(self, name):
        self.m_name             = name
    def GetName(self):
        return self.m_name
    def SetType(self, type):
        self.m_type             = type
    def GetType(self):
        return self.m_type

class EquationValue:
    def __init__(self, equation = '', value = 0.0):
        super().__init__()
        self.m_equation = equation
        self.m_value    = value
    def SetEquation(self, equation):
        self.m_equation = equation
    def GetEquation(self):
        return self.m_equation
    def SetValue(self, value):
        self.m_value = value
    def GetValue(self):
        return self.m_value

class Parameters:
    def __init__(self):
        super().__init__()
        self.m_equation_value_dic   = {}    # key : name, data : equationvalue
    def IsExistParameter(self, name):
        if name in self.m_equation_value_dic:
            return True
        else:
            return False
    def AddParameter(self, name, equation):
        if False == self.IsExistParameter(name):
            equation_value  = EquationValue(equation, 0.0)
            self.m_equation_value_dic[name] = equation_value
        else:
            equation_value  = self.m_equation_value_dic[name]
            equation_value.SetEquation(equation)

class Node(Object):
    def __init__(self, name = '', type = Type.INIT):
        super().__init__()
        self.m_name             = name
        self.m_type             = type
        self.m_insts            = []
    def AddInst(self, inst):
        self.m_insts.append(inst)
    def GetInsts(self):
        return self.m_insts

class Inst(Object, Parameters):
    def __init__(self, name = '', type = Type.INIT):
        super().__init__()
        self.m_name             = name
        self.m_type             = type
        self.m_nodes            = []
        self.m_cell             = None
    def AddNode(self, node):
        self.m_nodes.append(node)
    def GetNodes(self):
        return self.m_nodes
    def GetNode(self, pos):
        if pos < len(self.m_nodes):
            return self.m_nodes[pos]
        else:
            return None
    def SetCell(self, cell):
        self.m_cell = cell
    def GetCell(self):
        return self.m_cell

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
    def GetNetlistStr(self):
        match self.GetType():
            case Type.CELL_CELL:
                return self.GetNetlistStrCell()
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
    def GetNetlistStrCell(self):
        netlist_str     = ''
        netlist_str     += f'.subckt {self.GetName()}'
        pinnames        = []
        for pin in self.GetPins():
            pinnames.append(pin.GetName())
        netlist_str     += f" {' '.join(pinnames)}\n"
        netlist_str     += f'.ends'
        netlist_str     += f'\n'
        return netlist_str
    def GetNetlistStrModel(self):
        netlist_str     = ''
        netlist_str     += f'.model {self.GetName()} {GetTypeName(self.GetType())}'
        netlist_str     += f'\n'
        return netlist_str

class Netlist(Parameters):
    def __init__(self):
        super().__init__()
        self.m_cell_dic = {}
        self.m_top_cellname = k_TOP_CELLNAME
        self.m_top_cell = None
    def SetTopCellname(self, top_cellname):
        self.m_top_cellname = top_cellname
    def GetTopCellname(self):
        return self.m_top_cellname
    def SetTopCell(self, top_cell):
        self.m_top_cell = top_cell
    def GetTopCell(self):
        return self.m_top_cell
    def GetCellDic(self):
        return self.m_cell_dic
    def IsExistCell(self, name, type):
        key     = self.GetCellKey(name, type)
        if key in self.m_cell_dic:
            return True
        else:
            return False
    def GetCell(self, name, type):
        key     = self.GetCellKey(name, type)
        if key in self.m_cell_dic:
            return self.m_cell_dic[key]
        else:
            return None
    def AddCell(self, name, cell, type):
        key     = self.GetCellKey(name, type)
        if not key in self.m_cell_dic:
            self.m_cell_dic[key]   = cell
    def GetCellKey(self, name, type):
        return f'{name}:::{type}'
    def PrintInfo(self):
        print(f'# print info start ... {datetime.datetime.now()}')
        print(f'key(name:::type) #inst #node #pin')
        for key in self.m_cell_dic:
            cell    = self.m_cell_dic[key]
            print(f'{key} {len(cell.GetInstDic())} {len(cell.GetNodeDic())} {len(cell.GetPins())}')
        print(f'# print info end ... {datetime.datetime.now()}')
    def PrintNetlist(self):
        print(f'# print netlist start ... {datetime.datetime.now()}')
        netlist_str     = ''
        for key in self.m_cell_dic:
            cell            = self.m_cell_dic[key]
            netlist_str     += cell.GetNetlistStr()
        print(f'{netlist_str}')
        print(f'# print netlist end ... {datetime.datetime.now()}')