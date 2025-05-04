from .spiceutil_utils import Type


# name : public 변수
# _name : protected 변수
# __name : private 변수
class Object:
    def __init__(self, name="", type=Type.INIT):
        self.__name = name
        self.__type = type

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type
