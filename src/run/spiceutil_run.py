import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log


class Run:
    def __init__(self, log=None):
        self.m_log = log
        self.m_output_prefix = ""
        self.m_run = None
        self.m_filename = ""
        self.m_netlist = None
        # self.m_input_dic = {}

    def set_log(self, log):
        self.m_log = log

    def get_log(self):
        return self.m_log

    def set_run(self, run):
        self.m_run = run

    def get_run(self):
        return self.m_run

    def set_output_prefix(self, output_prefix):
        self.m_output_prefix = output_prefix

    def get_output_prefix(self):
        return self.m_output_prefix

    def set_filename(self, filename):
        self.m_filename = filename

    def get_filename(self):
        return self.m_filename

    def set_netlist(self, netlist):
        self.m_netlist = netlist

    def get_netlist(self):
        return self.m_netlist


#    def add_input(self, input_name, input_value):
#        if not input_name in self.m_input_dic:
#            self.m_input_dic[input_name] = input_value
#
#    def get_input_dic(self):
#        return self.m_input_dic
#
#    def get_input_value(self, input_name):
#        if input_name in self.m_input_dic:
#            return self.m_input_dic[input_name]
#        else:
#            return None
