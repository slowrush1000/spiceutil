import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils


class Input:
    def __init__(self):
        self.__args = None
        self.__output_prefix = "spiceutil"
        self.__func = ""
        self.__netlist_file_name = ""
        self.__topcell_name = ""
        self.__net_names = []
        self.__power_net_names = []
        self.__ground_net_names = []

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

    def get_inputs_str(self):
        s1 = f"args          : {' '.join(self.__args)}\n"
        s1 += f"output prefix   : {self.__output_prefix}\n"
        s1 += f"func            : {self.__func}\n"
        s1 += f"netlist file    : {self.__netlist_file_name}\n"
        s1 += f"topcell         : {self.__topcell_name}\n"
        s1 += f"nets            : {' '.join(self.__net_names)}\n"
        s1 += f"power nets      : {' '.join(self.__power_net_names)}\n"
        s1 += f"ground nets     : {' '.join(self.__ground_net_names)}\n"
        return s1
