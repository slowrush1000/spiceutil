import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import Const


class Input:
    def __init__(self):
        self.__args = None
        self.__output_prefix = "spiceutil"
        self.__func = ""
        self.__netlist_file_name = ""
        self.__topcell_name = Const().get_topcell_name()
        self.__net_names = []
        self.__power_net_names = []
        self.__ground_net_names = []
        self.__case_sense = False
        self.__dollar_comment = False  # $ is comments
        self.__debug = False
        self.__all_probe = False

    def set_args(self, args):
        self.__args = args

    def get_args(self):
        return self.__args

    def set_output_prefix(self, output_prefix):
        self.__output_prefix = output_prefix

    def get_output_prefix(self):
        return self.__output_prefix

    def set_func(self, func):
        self.__func = func

    def get_func(self):
        return self.__func

    def set_netlist_file_name(self, netlist_file_name):
        self.__netlist_file_name = netlist_file_name

    def get_netlist_file_name(self):
        return self.__netlist_file_name

    def set_topcell_name(self, topcell_name):
        self.__topcell_name = topcell_name

    def get_topcell_name(self):
        return self.__topcell_name

    def set_net_names(self, net_names):
        for net_name in net_names:
            self.__net_names.append(net_name)

    def get_net_names(self):
        return self.__net_names

    def set_power_net_names(self, power_net_names):
        for power_net_name in power_net_names:
            self.__power_net_names.append(power_net_name)

    def get_power_net_names(self):
        return self.__power_net_names

    def set_ground_net_names(self, ground_net_names):
        for ground_net_name in ground_net_names:
            self.__ground_net_names.append(ground_net_name)

    def get_ground_net_names(self):
        return self.__ground_net_names

    def set_case_sense(self, case_sense):
        self.__case_sense = case_sense

    def get_case_sense(self):
        return self.__case_sense

    def set_dollar_comment(self, dollar_comment):
        self.__dollar_comment = dollar_comment

    def get_dollar_comment(self):
        return self.__dollar_comment

    def set_debug(self, debug):
        self.__debug = debug

    def get_debug(self):
        return self.__debug

    def set_all_probe(self, all_probe):
        self.__all_probe = all_probe

    def get_all_probe(self):
        return self.__all_probe

    def get_inputs_str(self):
        s1 = f"args            : {' '.join(self.__args)}\n"
        s1 += f"output prefix   : {self.get_output_prefix()}\n"
        s1 += f"func            : {self.get_func()}\n"
        s1 += f"netlist file    : {self.get_netlist_file_name()}\n"
        s1 += f"topcell         : {self.get_topcell_name()}\n"
        s1 += f"nets            : {' '.join(self.get_net_names())}\n"
        s1 += f"power nets      : {' '.join(self.get_power_net_names())}\n"
        s1 += f"ground nets     : {' '.join(self.get_ground_net_names())}\n"
        s1 += f"case sense      : {self.get_case_sense()}\n"
        s1 += f"dollar comment  : {self.get_dollar_comment()}\n"
        s1 += f"debug           : {self.get_debug()}\n"
        s1 += f"all_probe       : {self.get_all_probe()}\n"
        return s1
