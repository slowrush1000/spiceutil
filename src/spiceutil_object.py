
from spiceutil_type import Type

class Object:
    def __init__(self, name = '', type = Type.INIT):
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