import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


class Object:
    def __init__(self, name="", type=utils.Type_tt.INIT, selected=False):
        super().__init__()
        self.__name = name
        self.__type = type
        self.__selected = selected

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

    def set_selected(self, selected):
        self.__selected = selected

    def get_selected(self):
        return self.__selected
