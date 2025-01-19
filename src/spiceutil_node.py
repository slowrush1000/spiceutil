
from spiceutil_type     import Type
from spiceutil_object   import Object

class Node(Object):
    def __init__(self, name = '', type = Type.INIT):
        self.m_name             = name
        self.m_type             = type
        self.m_insts            = []
    def AddInst(self, inst):
        self.m_insts.append(inst)
    def GetInsts(self):
        return self.m_insts