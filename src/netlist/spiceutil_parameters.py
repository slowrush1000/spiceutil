#
class EquationValue:
    def __init__(self, equation = '', value = 0.0):
        super().__init__()
        self.m_equation = equation
        self.m_value    = value
    def SetEquation(self, equation):
        self.m_equation = equation
    def GetEquation(self):
        return self.m_equation
    def SetValue(self, value):
        self.m_value = value
    def GetValue(self):
        return self.m_value
#
class Parameters:
    def __init__(self):
        super().__init__()
        self.m_equation_value_dic   = {}    # key : name, data : equationvalue
    def IsExistParameter(self, name):
        if name in self.m_equation_value_dic:
            return True
        else:
            return False
    def AddParameter(self, name, equation):
        if False == self.IsExistParameter(name):
            equation_value  = EquationValue(equation, 0.0)
            self.m_equation_value_dic[name] = equation_value
        else:
            equation_value  = self.m_equation_value_dic[name]
            equation_value.SetEquation(equation)