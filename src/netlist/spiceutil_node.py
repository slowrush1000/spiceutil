from .spiceutil_object import Object
from .spiceutil_utils import Type


class Node(Object):
    def __init__(self, name="", type=Type.INIT, selected=False):
        super().__init__(name, type, selected)
        self.m_inst_dic = {}

    def add_inst(self, name, inst):
        if not name in self.m_inst_dic:
            self.m_inst_dic[name] = inst

    def get_inst(self, name):
        if name in self.m_inst_dic:
            return self.m_inst_dic[name]
        else:
            return None
