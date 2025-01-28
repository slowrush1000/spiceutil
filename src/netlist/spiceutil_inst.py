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
        netlist_str     = f'{self.GetName()}'
        for node in self.m_nodes:
            netlist_str += f' {node.GetName()}'
        if GetDefaultRCell() == self.GetCell().GetName():
            pass
        elif GetDefaultLCell() == self.GetCell().GetName():
            pass
        elif GetDefaultCCell() == self.GetCell().GetName():
            pass
        else:
            netlist_str += f' {self.GetCell().GetName()}'
        for parameter_name in self.m_equation_value_dic:
            equation_value  = self.m_equation_value_dic[parameter_name]
            netlist_str += f" {parameter_name} = '{equation_value.GetEquation()}'"
        netlist_str     += '\n'
        return netlist_str