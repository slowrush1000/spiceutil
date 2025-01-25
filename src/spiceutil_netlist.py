
from spiceutil_type     import Type
from spiceutil_object   import Object
from spiceutil_node     import Node
from spiceutil_inst     import Inst
from spiceutil_parameters import Parameters
from spiceutil_cell     import Cell

class Netlist(Parameters):
    def __init__(self):
        self.m_cell_dic = {}
        self.m_top_cellname = 'xxx_top_xxx'
        self.m_top_cell = None
    def SetTopCellname(self, top_cellname):
        self.m_top_cellname = top_cellname
    def GetTopCellname(self):
        return self.m_top_cellname
    def SetTopCell(self, top_cell):
        self.m_top_cell = top_cell
    def GetTopCell(self):
        return self.m_top_cell
    def IsExistCell(self, name):
        if name in self.m_cell_dic:
            return True
        else:
            return False
    def GetCell(self, name):
        if name in self.m_cell_dic:
            return self.m_cell_dic[name]
        else:
            return None
    def AddCell(self, name, cell):
        if not name in self.m_cell_dic:
            self.m_cell_dic[name]   = cell