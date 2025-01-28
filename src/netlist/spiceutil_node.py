#
from .spiceutil_object   import Object
from .spiceutil_utils    import Type
#
class Node(Object):
    def __init__(self, name = '', type = Type.INIT):
        super().__init__()
        self.m_name             = name
        self.m_type             = type
        self.m_inst_dic         = {}
    def AddInst(self, name, inst):
        if not name in self.m_inst_dic:
            self.m_inst_dic[name]   = inst
    def GetInst(self, name):
        if name in self.m_inst_dic:
            return self.m_inst_dic[name]
        else:
            return None