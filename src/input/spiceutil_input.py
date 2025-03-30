import sys
import os
import logging
import getpass
import socket

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import log
import netlist
import version


class Input:
    def __init__(self):
        self.m_config_filename = ""
        self.m_args = []
        #
        self.m_run = ""
        self.m_output_prefix = ""
        self.m_spice_filename = ""
        self.m_top_cellname = netlist.get_k_default_top_cellname()
        self.m_netnames = []
        self.m_casesensitive = False
        self.m_dollar_comment = False
        self.m_all_probe = False
        self.m_is_write_1st_spc = False
        self.m_is_write_2nd_spc = False
        self.m_log_verbose = "INFO"
        self.m_text_width = 80
        self.m_flatten_delimiter = "_"
        #
        self.m_user = getpass.getuser()
        self.m_hostname = socket.gethostname()
        self.m_cwd = os.getcwd()
        #
        self.m_log = None
        self.m_version = version.Version()

    def set_config_filename(self, config_filename):
        self.m_config_filename = config_filename

    def get_config_filename(self):
        return self.m_config_filename

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

    def set_spice_filename(self, spice_filename):
        self.m_spice_filename = spice_filename

    def get_spice_filename(self):
        return self.m_spice_filename

    def set_top_cellname(self, top_cellname):
        self.m_top_cellname = top_cellname

    def get_top_cellname(self):
        return self.m_top_cellname

    def set_netnames(self, netnames):
        self.m_netnames = netnames

    def get_netnames(self):
        return self.m_netnames

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

    def set_flatten_delimiter(self, flatten_delimiter):
        self.m_flatten_delimiter = flatten_delimiter

    def get_flatten_delimiter(self):
        return self.m_flatten_delimiter

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

    def get_system_str(self):
        s = f"--------------------------------------------------------\n"
        s += f"{self.get_version().get_program()} {self.get_version().get_version()}\n"
        s += f"--------------------------------------------------------\n"
        s += f"user             : {self.get_user()}\n"
        s += f"hostname         : {self.get_hostname()}\n"
        s += f"cwd              : {self.get_cwd()}\n"
        s += f"--------------------------------------------------------"
        return s

    def get_str(self):
        s = f"--------------------------------------------------------\n"
        s += f"config file          : {self.get_config_filename()}\n"
        s += f"args                 : {' '.join(self.get_args())}\n"
        s += f"--------------------------------------------------------\n"
        s += f"run                  : {self.get_run()}\n"
        s += f"output prefix        : {self.get_output_prefix()}\n"
        s += f"spice file           : {self.get_spice_filename()}\n"
        s += f"top cell             : {self.get_top_cellname()}\n"
        s += f"netnames             : {' '.join(self.get_netnames())}\n"
        s += f"--------------------------------------------------------\n"
        s += f"casesensitive        : {self.get_casesensitive()}\n"
        s += f"dollar_comment       : {self.get_dollar_comment()}\n"
        s += f"write 1st spc        : {self.get_is_write_1st_spc()}\n"
        s += f"write 2nd spc        : {self.get_is_write_2nd_spc()}\n"
        s += f"log verbose          : {self.get_log_verbose()}\n"
        s += f"text width           : {self.get_text_width()}\n"
        s += f"flatten delimiter    : {self.get_flatten_delimiter()}\n"
        s += f"--------------------------------------------------------"
        return s
