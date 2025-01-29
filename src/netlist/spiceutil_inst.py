#
from .spiceutil_object      import Object
from .spiceutil_parameters  import Parameters
from .spiceutil_utils       import Type
from .spiceutil_utils       import GetDefaultRCell
from .spiceutil_utils       import GetDefaultLCell
from .spiceutil_utils       import GetDefaultCCell
#
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
    def GetNetlistStr(self):
        print(f'debug- {self.GetName()} {self.GetCell().GetName()}')
        for parameter_name_1 in self.m_equation_value_dic:
            equation_value_1    = self.m_equation_value_dic[parameter_name_1]
            print(f'debug- {parameter_name_1} : {equation_value_1.GetEquation()}')
        #
        netlist_str     = f'{self.GetName()}'
        for node in self.m_nodes:
            netlist_str += f' {node.GetName()}'
        #
        if (GetDefaultRCell() == self.GetCell().GetName()) and (Type.INST_R == self.GetType()):
            if GetDefaultRCell() in self.m_equation_value_dic:
                equation_value  = self.m_equation_value_dic[GetDefaultRCell()]
                netlist_str     += f' {equation_value.GetEquation()}'
        elif (GetDefaultLCell() == self.GetCell().GetName()) and (Type.INST_L == self.GetType()):
            if GetDefaultLCell() in self.m_equation_value_dic:
                equation_value  = self.m_equation_value_dic[GetDefaultLCell()]
                netlist_str     += f' {equation_value.GetEquation()}'
        elif (GetDefaultCCell() == self.GetCell().GetName()) and (Type.INST_C == self.GetType()):
            if GetDefaultCCell() in self.m_equation_value_dic:
                equation_value  = self.m_equation_value_dic[GetDefaultCCell()]
                netlist_str     += f' {equation_value.GetEquation()}'
        else:
            netlist_str += f' {self.GetCell().GetName()}'
        #
        for parameter_name in self.m_equation_value_dic:
            if (GetDefaultRCell() == self.GetCell().GetName()) or (GetDefaultLCell() == self.GetCell().GetName()) or (GetDefaultCCell() == self.GetCell().GetName()):
                continue
            equation_value  = self.m_equation_value_dic[parameter_name]
            netlist_str += f" {parameter_name} = '{equation_value.GetEquation()}'"
        return netlist_str
        #