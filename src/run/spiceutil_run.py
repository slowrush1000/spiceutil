import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import netlist


class Run:
    def __init__(self, t_input=None, t_netlist=None):
        self.m_input = t_input
        self.m_netlist = t_netlist

    def set_input(self, input):
        self.m_input = input

    def get_input(self):
        return self.m_input

    def set_netlist(self, netlist):
        self.m_netlist = netlist

    def get_netlist(self):
        return self.m_netlist
