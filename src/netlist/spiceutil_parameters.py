class EquationValue:
    def __init__(self, equation="", value=0.0):
        super().__init__()
        self.m_equation = equation
        self.m_value = value

    def set_equation(self, equation):
        self.m_equation = equation

    def get_equation(self):
        return self.m_equation

    def set_value(self, value):
        self.m_value = value

    def get_value(self):
        return self.m_value


class Parameters:
    def __init__(self):
        super().__init__()
        self.m_equation_value_dic = {}  # key : name, data : equationvalue

    def is_exist_parameter(self, name):
        if name in self.m_equation_value_dic:
            return True
        else:
            return False

    def add_parameter(self, name, equation):
        if False == self.is_exist_parameter(name):
            equation_value = EquationValue(equation, 0.0)
            self.m_equation_value_dic[name] = equation_value
        else:
            equation_value = self.m_equation_value_dic[name]
            equation_value.set_equation(equation)
