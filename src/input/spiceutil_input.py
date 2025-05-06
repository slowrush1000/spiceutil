import sys
import os
import logging
import getpass
import socket
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import log
import netlist
import version


class Input:
    def __init__(self):
        self.__config_file_name = ""
        self.__args = []
        #
        self.__runmode = netlist.Runmode.INIT
        self.__output_prefix = ""
        self.__spice_file_name = ""
        self.__top_cell_name = netlist.k_DEFAULT_TOP_CELL_NAME()
        self.__net_names = []
        self.__casesensitive = False
        self.__dollar_comment = False
        self.__all_probe = False
        self.__is_write_1st_spc = False
        self.__is_write_2nd_spc = False
        self.__log_verbose = "INFO"
        self.__text_width = 100
        self.__flatten_delim = "_"
        self.__malias = False
        #
        self.__user = getpass.getuser()
        self.__hostname = socket.gethostname()
        self.__cwd = os.getcwd()
        #
        self.__log = None
        self.__version = version.Version()
        self.__log_file_name = ""

    def set_config_file_name(self, config_file_name):
        self.__config_file_name = config_file_name

    def get_config_file_name(self):
        return self.__config_file_name

    def set_args(self, args):
        self.__args = args

    def get_args(self):
        return self.__args

    def set_runmode(self, runmode):
        self.__runmode = runmode

    def get_runmode(self):
        return self.__runmode

    def set_output_prefix(self, output_prefix):
        self.__output_prefix = output_prefix

    def get_output_prefix(self):
        return self.__output_prefix

    def set_spice_file_name(self, spice_file_name):
        self.__spice_file_name = spice_file_name

    def get_spice_file_name(self):
        return self.__spice_file_name

    def set_top_cell_name(self, top_cell_name):
        self.__top_cell_name = top_cell_name

    def get_top_cell_name(self):
        return self.__top_cell_name

    def set_net_names(self, net_names):
        self.__net_names = net_names

    def get_net_names(self):
        return self.__net_names

    def set_casesensitive(self, casesensitive):
        self.__casesensitive = casesensitive

    def get_casesensitive(self):
        return self.__casesensitive

    def set_dollar_comment(self, dollar_comment):
        self.__dollar_comment = dollar_comment

    def get_dollar_comment(self):
        return self.__dollar_comment

    def set_all_probe(self, all_probe):
        self.__all_probe = all_probe

    def get_all_probe(self):
        return self.__all_probe

    def set_is_write_1st_spc(self, is_write_1st_spc):
        self.__is_write_1st_spc = is_write_1st_spc

    def get_is_write_1st_spc(self):
        return self.__is_write_1st_spc

    def set_is_write_2nd_spc(self, is_write_2nd_spc):
        self.__is_write_2nd_spc = is_write_2nd_spc

    def get_is_write_2nd_spc(self):
        return self.__is_write_2nd_spc

    def set_log_verbose(self, log_verbose):
        self.__log_verbose = log_verbose

    def get_log_verbose(self):
        return self.__log_verbose

    def set_text_width(self, width):
        self.__text_width = width

    def get_text_width(self):
        return self.__text_width

    def set_flatten_delim(self, flatten_delim):
        self.__flatten_delim = flatten_delim

    def get_flatten_delim(self):
        return self.__flatten_delim

    def set_malias(self, malias):
        self.__malias = malias

    def get_malias(self):
        return self.__malias

    def get_user(self):
        return self.__user

    def get_hostname(self):
        return self.__hostname

    def get_cwd(self):
        return self.__cwd

    def set_log(self, log):
        self.__log = log

    def get_log(self):
        return self.__log

    def set_version(self, version):
        self.__version = version

    def get_version(self):
        return self.__version

    def set_log_file_name(self, log_file_name):
        self.__log_file_name = log_file_name

    def get_log_file_name(self):
        return self.__log_file_name

    def get_system_str(self, first_char="# "):
        s1 = f"{first_char}--------------------------------------------------------\n"
        s1 += f"{first_char}{self.get_version().get_program()} {self.get_version().get_version()}\n"
        s1 += f"{first_char}start at {datetime.datetime.now()}\n"
        s1 += f"{first_char}--------------------------------------------------------\n"
        s1 += f"{first_char}user     : {self.get_user()}\n"
        s1 += f"{first_char}hostname : {self.get_hostname()}\n"
        s1 += f"{first_char}cwd      : {self.get_cwd()}\n"
        s1 += f"{first_char}log file : {self.get_log_file_name()}\n"
        s1 += f"{first_char}--------------------------------------------------------"
        return s1

    def get_str(self):
        s1 = f"--------------------------------------------------------\n"
        s1 += f"config file          : {self.get_config_file_name()}\n"
        s1 += f"args                 : {' '.join(self.get_args())}\n"
        s1 += f"--------------------------------------------------------\n"
        s1 += f"runmode              : {self.get_runmode().name}\n"
        s1 += f"output prefix        : {self.get_output_prefix()}\n"
        s1 += f"spice file           : {self.get_spice_file_name()}\n"
        s1 += f"top cell             : {self.get_top_cell_name()}\n"
        s1 += f"net names            : {' '.join(self.get_net_names())}\n"
        s1 += f"--------------------------------------------------------\n"
        s1 += f"casesensitive        : {self.get_casesensitive()}\n"
        s1 += f"dollar_comment       : {self.get_dollar_comment()}\n"
        s1 += f"all probe            : {self.get_all_probe()}\n"
        s1 += f"write 1st spc        : {self.get_is_write_1st_spc()}\n"
        s1 += f"write 2nd spc        : {self.get_is_write_2nd_spc()}\n"
        s1 += f"log verbose          : {self.get_log_verbose()}\n"
        s1 += f"text width           : {self.get_text_width()}\n"
        s1 += f"flatten delim        : {self.get_flatten_delim()}\n"
        s1 += f"malias               : {self.get_malias()}\n"
        s1 += f"--------------------------------------------------------"
        return s1
