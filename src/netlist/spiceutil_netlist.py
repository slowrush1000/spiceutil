from .spiceutil_cell import Cell
from .spiceutil_utils import *


class Netlist:
    def __init__(self):
        self.__cell_dic = {}  # key : cell_key : data : cell
        self.__top_cell_name = k_DEFAULT_TOP_CELL_NAME()
        self.__top_cell = None
        self.__cell_key_delim = "="
        self.__global_node_names = []
        self.__global_node_names_set = set(self.__global_node_names)
        #
        self.__cell_keys = []

    def set_top_cell_name(self, top_cell_name):
        self.__top_cell_name = top_cell_name

    def get_top_cell_name(self):
        return self.__top_cell_name

    def set_top_cell(self, top_cell):
        self.__top_cell = top_cell

    def get_top_cell(self):
        return self.__top_cell

    def set_cell_key_delim(self, cell_key_delim):
        self.__cell_key_delim = cell_key_delim

    def get_cell_key_delim(self):
        return self.__cell_key_delim

    def get_cell_dic(self):
        return self.__cell_dic

    def get_cell_by_cell_key(self, cell_key):
        if cell_key in self.__cell_dic:
            return self.__cell_dic[cell_key]
        else:
            return None

    def get_cell(self, name, type):
        cell_key = get_cell_key(name, type)
        return self.get_cell_by_cell_key(cell_key)

    def add_cell(self, cell):
        cell_key = get_cell_key(cell.get_name(), cell.get_type())
        if not cell_key in self.__cell_dic:
            self.__cell_dic[cell_key] = cell

    def split_cell_key(self, cell_key):
        tokens = cell_key.split(self.get_cell_key_delim())
        cell_name = tokens[0]
        cell_type = Type[tokens[1].strip()]
        return cell_name, cell_type

    def add_global_net_name(self, global_netname):
        self.__global_node_names.append(global_netname)

    def get_global_net_names(self):
        return self.__global_node_names

    def make_global_net_names_set(self):
        self.__global_node_names_set = set(self.__global_node_names)

    def get_global_net_names_set(self):
        return self.__global_node_names_set

    def get_cell_keys(self):
        return self.__cell_keys

    def add_cell_key(self, cell_key):
        self.__cell_keys.append(cell_key)

    def get_cell_summary_str(self):
        s1 = self.get_cell_summary_str_global()
        s1 += self.get_cell_summary_str_cells()
        return s1

    def get_cell_summary_str_global(self):
        s1 = f"-----------------------------------------------------------------------------------------------------------------\n"
        s1 += f"global\n"
        s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
        s1 += f"{'key':40s}"
        s1 += f"{'#inst':>15s}"
        s1 += f"{'#node':>15s}"
        s1 += f"{'#pin':>15s}"
        s1 += f"{'#inst_count':>15s}\n"
        s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
        for cell_key in self.get_cell_keys():
            cell = self.get_cell_by_cell_key(cell_key)
            if None == cell:
                continue
            s1 += f"{cell_key:40s}"
            s1 += f"{len(cell.get_inst_dic()):15d}"
            s1 += f"{len(cell.get_node_dic()):15d}"
            s1 += f"{len(cell.get_pins()):15d}"
            s1 += f"{cell.get_inst_count():15d}\n"
        s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
        if 0 < len(self.get_global_net_names_set()):
            for global_net_name in self.get_global_net_names_set():
                s1 += f"global_net {global_net_name}\n"
            s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
        return s1

    def get_cell_summary_str_cells(self):
        s1 = f""
        for cell_key in self.get_cell_keys():
            cell = self.get_cell_by_cell_key(cell_key)
            if None == cell:
                continue
            if 0 < len(cell.get_cell_dic()):
                s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
                s1 += f"local(from {cell.get_name()})\n"
                s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
                s1 += self.get_cell_summary_str_cell(cell)
                s1 += f"-----------------------------------------------------------------------------------------------------------------\n"
        return s1

    def get_cell_summary_str_cell(self, cell):
        s1 = f""
        for cell_key in cell.get_cell_dic():
            t_cell = cell.get_cell_by_cell_key(cell_key)
            if None == t_cell:
                break
            s1 += f"{cell_key:40s}"
            s1 += f"{len(t_cell.get_inst_dic()):15d}"
            s1 += f"{len(t_cell.get_node_dic()):15d}"
            s1 += f"{len(t_cell.get_pins()):15d}"
            s1 += f"{t_cell.get_inst_count():15d}\n"
        return s1


#    def get_info_str(self):
#        info_str = f"--------------------------------------------------------"
#        #
#        info_str += f"\nkey(name{self.get_cell_key_delim()
#                               }type) #inst #node #pin"
#        info_str += f"\n--------------------------------------------------------"
#        #
#        for key in self.m_cell_dic:
#            cell = self.m_cell_dic[key]
#            info_str += f"\n{key} {len(cell.get_inst_dic())} {len(cell.get_node_dic())} {len(cell.get_pins())}"
#        #
#        if None != self.m_global_nodenames_set:
#            info_str += f"\nglobal_netname"
#            for global_netname in self.m_global_nodenames_set:
#                info_str += f" {global_netname}"
#        #
#        return info_str
#
#    def get_inst_info_str(self):
#        info_str = f"--------------------------------------------------------"
#        info_str += f"\ninst_name cell_name cell_type"
#        info_str += f"\n--------------------------------------------------------"
#        # for key in self.m_cell_dic:
#        #    cell = self.m_cell_dic[key]
#        #    info_str += f"{cell.get_inst_info_str()}"
#        return info_str
#
#    def print_info(self, logger=None):
#        if None == logger:
#            print(f"# print cell info start ... {datetime.datetime.now()}")
#            print(f"{self.get_info_str()}")
#            print(f"# print cell info end ... {datetime.datetime.now()}\n")
#        else:
#            logger.info(f"# print cell info start ... {datetime.datetime.now()}")
#            logger.info(f"{self.get_info_str()}")
#            logger.info(f"# print cell info end ... {datetime.datetime.now()}\n")
#
#    def print_inst_info(self, logger=None):
#        if None == logger:
#            print(f"# print inst info start ... {datetime.datetime.now()}")
#            print(f"{self.get_inst_info_str()}")
#            print(f"# print inst info end ... {datetime.datetime.now()}\n")
#        else:
#            logger.info(f"# print inst info start ... {datetime.datetime.now()}")
#            logger.info(f"{self.get_inst_info_str()}")
#            logger.info(f"# print inst info end ... {datetime.datetime.now()}\n")
#
