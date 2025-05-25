import inspect
import os
import socket
import sys
import textwrap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.type_tt import Type_tt
from version import Version


class Utils:
    def get_first_char_inst(self, type):
        k_DEFAULT_FIRST_CHAR_DIC = {
            Type_tt.INST_R: "r",
            Type_tt.INST_L: "l",
            Type_tt.INST_C: "c",
            Type_tt.INST_K: "k",
            Type_tt.INST_VS: "v",
            Type_tt.INST_CS: "i",
            Type_tt.INST_VCVS: "e",
            Type_tt.INST_CCVS: "g",
            Type_tt.INST_VCCS: "h",
            Type_tt.INST_CCCS: "f",
            Type_tt.INST_DIODE: "d",
            Type_tt.INST_MOSFET: "m",
            Type_tt.INST_BJT: "q",
            Type_tt.INST_JFET: "j",
            Type_tt.INST_INST: "x",
        }
        if type in k_DEFAULT_FIRST_CHAR_DIC:
            return k_DEFAULT_FIRST_CHAR_DIC[type]
        else:
            return "*"

    def get_k_default_cellname_set(self):
        k_DEFAULT_CELLLNAMES = ["r", "l", "c", "k", "v", "i", "e", "g", "h", "f"]
        k_DEFAULT_CELLNAME_SET = set(k_DEFAULT_CELLLNAMES)
        return k_DEFAULT_CELLNAME_SET

    def get_subckt_types_set(self):
        k_SUBCKT_TYPES = [
            Type_tt.CELL_CELL_DIODE,
            Type_tt.CELL_CELL_NMOS,
            Type_tt.CELL_CELL_PMOS,
            Type_tt.CELL_CELL_NPN,
            Type_tt.CELL_CELL_PNP,
            Type_tt.CELL_CELL_NJF,
            Type_tt.CELL_CELL_PJF,
        ]
        k_SUBCKT_TYPES_SET = set(k_SUBCKT_TYPES)
        return k_SUBCKT_TYPES_SET

    def is_subckt_type(self, type):
        # subckt_types = get_subckt_types()
        # subckt_types_set = set(k_SUBCKT_TYPES)
        if type in self.get_subckt_types_set():
            return True
        else:
            return False

    def get_device_types(self):
        return [
            Type_tt.CELL_DIODE,
            Type_tt.CELL_NMOS,
            Type_tt.CELL_PMOS,
            Type_tt.CELL_NPN,
            Type_tt.CELL_PNP,
            Type_tt.CELL_NJF,
            Type_tt.CELL_PJF,
        ]

    def get_type_name(self, type):
        match type:
            case Type_tt.CELL_R:
                return "r"
            case Type_tt.CELL_L:
                return "l"
            case Type_tt.CELL_C:
                return "c"
            case Type_tt.CELL_K:
                return "k"
            case Type_tt.CELL_DIODE:
                return "d"
            case Type_tt.CELL_NMOS:
                return "nmos"
            case Type_tt.CELL_PMOS:
                return "pmos"
            case Type_tt.CELL_NPN:
                return "npn"
            case Type_tt.CELL_PNP:
                return "pnp"
            case Type_tt.CELL_NJF:
                return "njf"
            case Type_tt.CELL_PJF:
                return "pjf"
            case Type_tt.CELL_VS:
                return "vs"
            case Type_tt.CELL_CS:
                return "cs"
            case Type_tt.CELL_VCVS:
                return "vcvs"
            case Type_tt.CELL_CCVS:
                return "ccvs"
            case Type_tt.CELL_VCCS:
                return "vccs"
            case Type_tt.CELL_CCCS:
                return "cccs"
            case _:
                return ""

    def get_error_str(self, msg):
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        function_name = frame.f_code.co_name
        line_number = frame.f_lineno
        return f"{msg}({os.path.basename(filename)}:{function_name}:{line_number})"

    def get_netname(self, hier_netname):
        return hier_netname.split(".")[-1]

    def write_wrap_line(self, file, line, textwidth=100):
        wrap_lines = textwrap.wrap(
            line,
            width=textwidth,
            subsequent_indent="+ ",
            break_long_words=False,
            break_on_hyphens=False,
        )
        for wrap_line in wrap_lines:
            file.write(f"{wrap_line}")

    def get_system_str(self, first_words):
        s1 = f"{first_words} made by : {Version().get_program_version()}\n"
        s1 += f"{first_words} user    : {os.getlogin()}\n"
        s1 += f"{first_words} cwd     : {os.getcwd()}\n"
        s1 += f"{first_words} host    : {socket.gethostname()}\n"
        return s1
