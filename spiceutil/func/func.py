import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from input import Input
from log import Log
from netlist import Netlist


class Func:
    def __init__(self, t_input=None, t_log=None, t_netlist=None):
        self.__input = t_input
        self.__log = t_log
        self.__netlist = t_netlist

    def set_input(self, t_input):
        self.__input = t_input

    def get_input(self):
        return self.__input

    def set_log(self, t_log):
        self.__log = t_log

    def get_log(self):
        return self.__log

    def set_netlist(self, t_netlist):
        self.__netlist = t_netlist

    def get_netlist(self):
        return self.__netlist
