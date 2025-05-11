from .spiceutil_object import Object
from .spiceutil_param import Param
from .spiceutil_utils import Type


class Node(Object):
    def __init__(self, name="", type=Type.INIT):
        super().__init__(name, type)
        self.__insts = []
        self.__param = Param()

    def add_inst(self, inst):
        self.__insts.append(inst)

    def get_insts(self):
        return self.__insts

    def get_inst(self, pos):
        if pos < len(self.__insts):
            return self.__insts[pos]
        else:
            return None

    def set_param(self, param):
        self.__param = param

    def get_param(self):
        return self.__param
