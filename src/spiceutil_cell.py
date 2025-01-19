
from spiceutil_type     import Type
from spiceutil_object   import Object
from spiceutil_node     import Node
from spiceutil_inst     import Inst

class Cell(Object):
    def __init__(self, name = '', type = Type.INIT):
        self.m_name     = name
        self.m_type     = type
        self.m_inst_dic = {}    # key : name, data : inst
        self.m_node_dic = {}    # key : name, data : node
        self.m_pins     = []
    def IsExistInst(self, name):
        if name in self.m_inst_dic:
            return True
        else:
            return False
    def AddInst(self, name, inst):
        if not name in self.m_inst_dic:
            self.m_inst_dic[inst_name]  = inst
    def GetInst(self, name):
        if True == self.IsExistInst(name):
            return self.m_inst_dic[name]
        else:
            return None
    def IsExistNode(self, name):
        if name in self.m_node_dic:
            return True
        else:
            return False
    def AddNode(self, name, node):
        if not name in self.m_node_dic:
            self.m_node_dic[node_name]  = node
    def GetNode(self, name):
        if True == self.IsExistNode(name):
            return self.m_node_dic[name]
        else:
            return None
    def AddPin(self, name, pin):
        if not name in self.m_node_dic:
            self.m_node_dic[node_name]  = node
            self.m_pins.append(pin)