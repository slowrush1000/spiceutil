
from spiceutil_type     import Type
from spiceutil_object   import Object
from spiceutil_node     import Node

class Inst(Object):
    def __init__(self, name = '', type = Type.INIT):
        self.m_name             = name
        self.m_type             = type
        self.m_nodes            = []
        self.m_cellname         = ''
    def AddNode(self, node):
        self.m_nodes.append(node)
    def GetNodes(self):
        return self.m_nodes
    def GetNode(self, pos):
        if pos < len(self.m_nodes):
            return self.m_nodes[pos]
        else:
            return None
    def SetCellname(self, cellname):
        self.m_cellname         = cellname
    def GetCellname(self):
        return self.m_cellname