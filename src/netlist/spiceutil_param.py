from .spiceutil_equation import Equation


class Param:
    def __init__(self):
        self.__variable_names = []
        self.__equation_dic = {}  # key : name, data: Equation

    def get_variable_names(self):
        return self.__variable_names

    def get_equation_dic(self):
        return self.__equation_dic

    def add_equation(self, variable_name, equation_s, equation_value):
        if not variable_name in self.__equation_dic:
            self.__equation_dic[variable_name] = Equation(equation_s, equation_value)
            self.__variable_names.append(variable_name)

    def get_equation(self, variable_name):
        if variable_name in self.__equation_dic:
            return self.__equation_dic[variable_name]
        else:
            return None
