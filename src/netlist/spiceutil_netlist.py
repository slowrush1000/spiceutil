import datetime
import textwrap
from .spiceutil_parameters import Parameters
from .spiceutil_utils import k_TOP_CELLNAME
from .spiceutil_utils import Type
from .spiceutil_utils import get_program
from .spiceutil_utils import get_version


class Netlist(Parameters):
    def __init__(self):
        super().__init__()
        self.m_cell_dic = {}
        self.m_top_cellname = k_TOP_CELLNAME
        self.m_top_cell = None
        self.m_cell_key_delim = "="

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

    def get_info_str(self):
        info_str = ""
        info_str += f"key(name{self.get_cell_key_delim()
                               }type) #inst #node #pin #inst\n"
        for key in self.m_cell_dic:
            cell = self.m_cell_dic[key]
            info_str += f"{key} {len(cell.get_inst_dic())} {len(cell.get_node_dic())} {
                len(cell.get_pins())} {cell.get_inst_size()}\n"
        return info_str

    def get_inst_info_str(self):
        info_str = f"inst_name cell_name cell_type\n"
        for key in self.m_cell_dic:
            cell = self.m_cell_dic[key]
            info_str += f"{cell.get_inst_info_str()}"
        return info_str

    def print_info(self, logger=None):
        if None == logger:
            print(f"# print info start ... {datetime.datetime.now()}")
            print(f"{self.get_info_str()}")
            print(f"# print info end ... {datetime.datetime.now()}")
        else:
            logger.info(f"# print info start ... {datetime.datetime.now()}")
            logger.info(f"{self.get_info_str()}")
            logger.info(f"# print info end ... {datetime.datetime.now()}")

    def print_inst_info(self, logger=None):
        if None == logger:
            print(f"# print inst info start ... {datetime.datetime.now()}")
            print(f"{self.get_inst_info_str()}")
            print(f"# print inst info end ... {datetime.datetime.now()}")
        else:
            logger.info(f"# print inst info start ... {datetime.datetime.now()}")
            logger.info(f"{self.get_inst_info_str()}")
            logger.info(f"# print inst info end ... {datetime.datetime.now()}")

    def get_netlist_str(self):
        netlist_str = []
        #
        for key in self.m_cell_dic:
            cell = self.m_cell_dic[key]
            if k_TOP_CELLNAME == cell.get_name():
                continue
            netlist_str += cell.get_netlist_str()
        #
        k_top_cell_key = self.get_cell_key(k_TOP_CELLNAME, Type.CELL_CELL)
        if k_top_cell_key in self.m_cell_dic:
            cell = self.m_cell_dic[k_top_cell_key]
            netlist_str += cell.get_netlist_str(False)
        #
        return netlist_str

    def print_netlist(self, logger=None, filename=None, width=120):
        if (None == logger) and (None == filename):
            print(f"# print netlist start ... {datetime.datetime.now()}")
            for netlist_line in self.get_netlist_str():
                wrap_netlist_lines = textwrap.wrap(
                    netlist_line,
                    width=width,
                    subsequent_indent="+ ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                for wrap_netlist_line in wrap_netlist_lines:
                    print(f"{wrap_netlist_line}")
            print(f"# print netlist end ... {datetime.datetime.now()}")
        elif (None == logger) and (None != filename):
            print(f"# print netlist start ... {datetime.datetime.now()}")
            print(f"netlist file : {filename}")
            f = open(filename, "wt")
            for netlist_line in self.get_netlist_str():
                wrap_netlist_lines = textwrap.wrap(
                    netlist_line,
                    width=width,
                    subsequent_indent="+ ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                for wrap_netlist_line in wrap_netlist_lines:
                    f.write(f"{wrap_netlist_line}\n")
            f.close()
            print(f"# print netlist end ... {datetime.datetime.now()}")
        elif (None != logger) and (None == filename):
            logger.info(f"# print netlist start ... {datetime.datetime.now()}")
            for netlist_line in self.get_netlist_str():
                wrap_netlist_lines = textwrap.wrap(
                    netlist_line,
                    width=width,
                    subsequent_indent="+ ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                for wrap_netlist_line in wrap_netlist_lines:
                    logger.info(f"{wrap_netlist_line}")
            logger.info(f"# print netlist end ... {datetime.datetime.now()}")
        elif (None != logger) and (None != filename):
            logger.info(f"# print netlist start ... {datetime.datetime.now()}")
            logger.info(f"netlist file : {filename}")
            f = open(filename, "wt")
            for netlist_line in self.get_netlist_str():
                wrap_netlist_lines = textwrap.wrap(
                    netlist_line,
                    width=width,
                    subsequent_indent="+ ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                for wrap_netlist_line in wrap_netlist_lines:
                    f.write(f"{wrap_netlist_line}\n")
            f.close()
            logger.info(f"# print netlist end ... {datetime.datetime.now()}")
