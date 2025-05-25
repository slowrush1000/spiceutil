class EquationValue:
    def __init__(self, equation="", value=0.0):
        self.__equation = equation
        self.__value = value

    def set_equation(self, equation):
        self.__equation = equation

    def get_equation(self):
        return self.__equation

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value


class Parameters:
    def __init__(self):
        super().__init__()
        self.__equation_value_dic = {}  # key : name, data : EquationValue
        self.__names = []

    def get_equation_value_dic(self):
        return self.__equation_value_dic

    def get_names(self):
        return self.__names

    def is_in(self, name):
        if name in self.__equation_value_dic:
            return True
        else:
            return False

    def add_parameter(self, name, equation):
        if False == self.is_in(name):
            equation_value = EquationValue(equation, 0.0)
            self.__equation_value_dic[name] = equation_value
            self.__names.append(name)
        else:
            equation_value = self.__equation_value_dic[name]
            equation_value.set_equation(equation)
