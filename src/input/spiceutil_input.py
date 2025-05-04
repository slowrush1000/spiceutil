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
        self.m_config_file_name = ""
        self.m_args = []
        #
        self.m_run = ""
        self.m_output_prefix = ""
        self.m_spice_file_name = ""
        self.m_top_cell_name = netlist.k_DEFAULT_TOP_CELL_NAME()
        self.m_net_names = []
        self.m_casesensitive = False
        self.m_dollar_comment = False
        self.m_all_probe = False
        self.m_is_write_1st_spc = False
        self.m_is_write_2nd_spc = False
        self.m_log_verbose = "INFO"
        self.m_text_width = 100
        self.m_flatten_delim = "_"
        #
        self.m_user = getpass.getuser()
        self.m_hostname = socket.gethostname()
        self.m_cwd = os.getcwd()
        #
        self.m_log = None
        self.m_version = version.Version()

    def set_config_file_name(self, config_file_name):
        self.m_config_file_name = config_file_name

    def get_config_file_name(self):
        return self.m_config_file_name

    def set_args(self, args):
        self.m_args = args

    def get_args(self):
        return self.m_args

    def set_run(self, run):
        self.m_run = run

    def get_run(self):
        return self.m_run

    def set_output_prefix(self, output_prefix):
        self.m_output_prefix = output_prefix

    def get_output_prefix(self):
        return self.m_output_prefix

    def set_spice_file_name(self, spice_file_name):
        self.m_spice_file_name = spice_file_name

    def get_spice_file_name(self):
        return self.m_spice_file_name

    def set_top_cell_name(self, top_cell_name):
        self.m_top_cell_name = top_cell_name

    def get_top_cell_name(self):
        return self.m_top_cell_name

    def set_net_names(self, net_names):
        self.m_net_names = net_names

    def get_net_names(self):
        return self.m_net_names

    def set_casesensitive(self, casesensitive):
        self.m_casesensitive = casesensitive

    def get_casesensitive(self):
        return self.m_casesensitive

    def set_dollar_comment(self, dollar_comment):
        self.m_dollar_comment = dollar_comment

    def get_dollar_comment(self):
        return self.m_dollar_comment

    def set_all_probe(self, all_probe):
        self.m_all_probe = all_probe

    def get_all_probe(self):
        return self.m_all_probe

    def set_is_write_1st_spc(self, is_write_1st_spc):
        self.m_is_write_1st_spc = is_write_1st_spc

    def get_is_write_1st_spc(self):
        return self.m_is_write_1st_spc

    def set_is_write_2nd_spc(self, is_write_2nd_spc):
        self.m_is_write_2nd_spc = is_write_2nd_spc

    def get_is_write_2nd_spc(self):
        return self.m_is_write_2nd_spc

    def set_log_verbose(self, log_verbose):
        self.m_log_verbose = log_verbose

    def get_log_verbose(self):
        return self.m_log_verbose

    def set_text_width(self, width):
        self.m_text_width = width

    def get_text_width(self):
        return self.m_text_width

    def set_flatten_delim(self, flatten_delim):
        self.m_flatten_delim = flatten_delim

    def get_flatten_delim(self):
        return self.m_flatten_delim

    def get_user(self):
        return self.m_user

    def get_hostname(self):
        return self.m_hostname

    def get_cwd(self):
        return self.m_cwd

    def set_log(self, log):
        self.m_log = log

    def get_log(self):
        return self.m_log

    def set_version(self, version):
        self.m_version = version

    def get_version(self):
        return self.m_version

    def get_system_str(self, first_char="# "):
        s1 = f"{first_char}--------------------------------------------------------\n"
        s1 += f"{first_char}{self.get_version().get_program()} {self.get_version().get_version()}\n"
        s1 += f"{first_char}start at {datetime.datetime.now()}\n"
        s1 += f"{first_char}--------------------------------------------------------\n"
        s1 += f"{first_char}user     : {self.get_user()}\n"
        s1 += f"{first_char}hostname : {self.get_hostname()}\n"
        s1 += f"{first_char}cwd      : {self.get_cwd()}\n"
        s1 += f"{first_char}--------------------------------------------------------"
        return s1

    def get_str(self):
        s1 = f"--------------------------------------------------------\n"
        s1 += f"config file          : {self.get_config_file_name()}\n"
        s1 += f"args                 : {' '.join(self.get_args())}\n"
        s1 += f"--------------------------------------------------------\n"
        s1 += f"run                  : {self.get_run()}\n"
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
        s1 += f"--------------------------------------------------------"
        return s1
