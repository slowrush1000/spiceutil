import datetime
from .spiceutil_parameters import Parameters
from .spiceutil_utils import *


class Netlist(Parameters):
    def __init__(self):
        super().__init__()
        self.m_cell_dic = {}
        self.m_top_cellname = get_k_default_top_cellname()
        self.m_top_cell = None
        self.m_cell_key_delim = "="
        self.m_global_nodenames = []
        self.m_global_nodenames_set = set(self.m_global_nodenames)
        self.m_keys = []

    def set_top_cellname(self, top_cellname):
        self.m_top_cellname = top_cellname

    def get_top_cellname(self):
        return self.m_top_cellname

    def set_top_cell(self, top_cell):
        self.m_top_cell = top_cell

    def get_top_cell(self):
        return self.m_top_cell

    def set_cell_key_delim(self, cell_key_delim):
        self.m_cell_key_delim = cell_key_delim

    def get_cell_key_delim(self):
        return self.m_cell_key_delim

    def get_cell_dic(self):
        return self.m_cell_dic

    def is_exist_cell(self, name, type):
        key = self.get_cell_key(name, type)
        if key in self.m_cell_dic:
            return True
        else:
            return False

    def get_cell(self, name, type):
        key = self.get_cell_key(name, type)
        if key in self.m_cell_dic:
            return self.m_cell_dic[key]
        else:
            return None

    def get_cell_by_key(self, key):
        if key in self.m_cell_dic:
            return self.m_cell_dic[key]
        else:
            return None

    def add_cell(self, name, cell, type):
        key = self.get_cell_key(name, type)
        if not key in self.m_cell_dic:
            self.m_cell_dic[key] = cell

    def get_cell_key(self, name, type):
        return f"{name}{self.get_cell_key_delim()}{type}"

    def add_global_netname(self, global_netname):
        self.m_global_nodenames.append(global_netname)

    def get_global_netnames(self):
        return self.m_global_nodenames

    def make_global_netnames_set(self):
        self.m_global_nodenames_set = set(self.m_global_nodenames)

    def get_global_netnames_set(self):
        return self.m_global_nodenames_set

    def add_key(self, key):
        self.m_keys.append(key)

    def get_key(self):
        return self.m_keys

    def get_info_str(self):
        info_str = f"--------------------------------------------------------"
        #
        info_str += f"\nkey(name{self.get_cell_key_delim()
                               }type) #inst #node #pin"
        info_str += f"\n--------------------------------------------------------"
        #
        for key in self.m_cell_dic:
            cell = self.m_cell_dic[key]
            info_str += f"\n{key} {len(cell.get_inst_dic())} {len(cell.get_node_dic())} {len(cell.get_pins())}"
        #
        if None != self.m_global_nodenames_set:
            info_str += f"\nglobal_netname"
            for global_netname in self.m_global_nodenames_set:
                info_str += f" {global_netname}"
        #
        return info_str

    def get_inst_info_str(self):
        info_str = f"--------------------------------------------------------"
        info_str += f"\ninst_name cell_name cell_type"
        info_str += f"\n--------------------------------------------------------"
        # for key in self.m_cell_dic:
        #    cell = self.m_cell_dic[key]
        #    info_str += f"{cell.get_inst_info_str()}"
        return info_str

    def print_info(self, logger=None):
        if None == logger:
            print(f"# print cell info start ... {datetime.datetime.now()}")
            print(f"{self.get_info_str()}")
            print(f"# print cell info end ... {datetime.datetime.now()}\n")
        else:
            logger.info(f"# print cell info start ... {datetime.datetime.now()}")
            logger.info(f"{self.get_info_str()}")
            logger.info(f"# print cell info end ... {datetime.datetime.now()}\n")

    def print_inst_info(self, logger=None):
        if None == logger:
            print(f"# print inst info start ... {datetime.datetime.now()}")
            print(f"{self.get_inst_info_str()}")
            print(f"# print inst info end ... {datetime.datetime.now()}\n")
        else:
            logger.info(f"# print inst info start ... {datetime.datetime.now()}")
            logger.info(f"{self.get_inst_info_str()}")
            logger.info(f"# print inst info end ... {datetime.datetime.now()}\n")
