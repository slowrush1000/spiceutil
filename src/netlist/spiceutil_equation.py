class Equation:
    def __init__(self, str="", value=0.0):
        self.__s = str
        self.__value = value

    def set_s(self, s):
        self.__s = s

    def get_s(self):
        return self.__s

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value
