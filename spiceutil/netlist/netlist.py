import datetime
import os
import sys

from .parameters import Parameters

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


class Netlist(Parameters):
    def __init__(self):
        super().__init__()
        self.__cell_dic = {}
        self.__topcell_name = utils.Utils().get_k_topcell_name()
        self.__topcell = None
        self.__cell_key_delim = "="
        self.__global_nodenames = []
        self.__global_nodenames_set = set(self.__global_nodenames)
        self.__keys = []

    def set_topcell_name(self, top_cellname):
        self.__topcell_name = top_cellname

    def get_topcell_name(self):
        return self.__topcell_name

    def get_topcell(self, top_cell):
        self.__topcell = top_cell

    def get_topcell(self):
        return self.__topcell

    def set_cell_key_delim(self, cell_key_delim):
        self.__cell_key_delim = cell_key_delim

    def get_cell_key_delim(self):
        return self.__cell_key_delim

    def get_cell_dic(self):
        return self.__cell_dic

    def is_in_cell(self, name, type):
        key = self.get_cell_key(name, type)
        if key in self.__cell_dic:
            return True
        else:
            return False

    def get_cell(self, name, type):
        key = self.get_cell_key(name, type)
        if key in self.__cell_dic:
            return self.__cell_dic[key]
        else:
            return None

    def get_cell_by_key(self, key):
        if key in self.__cell_dic:
            return self.__cell_dic[key]
        else:
            return None

    def add_cell(self, name, cell, type):
        key = self.get_cell_key(name, type)
        if not key in self.__cell_dic:
            self.__cell_dic[key] = cell

    def get_cell_key(self, name, type):
        return f"{name}{self.get_cell_key_delim()}{type}"

    def add_global_netname(self, global_netname):
        self.__global_nodenames.append(global_netname)

    def get_global_netnames(self):
        return self.__global_nodenames

    def make_global_netnames_set(self):
        self.__global_nodenames_set = set(self.__global_nodenames)

    def get_global_netnames_set(self):
        return self.__global_nodenames_set

    def add_key(self, key):
        self.__keys.append(key)

    def get_key(self):
        return self.__keys

    def get_info_str(self):
        info_str = f"--------------------------------------------------------"
        info_str += f"\nkey(name{self.get_cell_key_delim()
                               }type) #inst #node #pin"
        info_str += f"\n--------------------------------------------------------"
        for key in self.__cell_dic:
            cell = self.__cell_dic[key]
            info_str += f"\n{key} {len(cell.get_inst_dic())} {len(cell.get_node_dic())} {len(cell.get_pins())}"
        if None != self.__global_nodenames_set:
            info_str += f"\nglobal_netname"
            for global_netname in self.__global_nodenames_set:
                info_str += f" {global_netname}"
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
