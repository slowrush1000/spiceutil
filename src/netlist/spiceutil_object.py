from .spiceutil_utils import Type


class Object:
    def __init__(self, name="", type=Type.INIT, selected=False):
        super().__init__()
        self.m_name = name
        self.m_type = type
        self.m_selected = selected

    def set_name(self, name):
        self.m_name = name

    def get_name(self):
        return self.m_name

    def set_type(self, type):
        self.m_type = type

    def get_type(self):
        return self.m_type

    def set_selected(self, selected):
        self.m_selected = selected

    def get_selected(self):
        return self.m_selected
