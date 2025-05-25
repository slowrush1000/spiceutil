from enum import Enum, auto
import inspect
import textwrap
import os


class Type(Enum):
    INIT = auto()
    #
    NODE_PIN = auto()
    NODE_NODE = auto()
    #
    CELL_R = auto()
    CELL_L = auto()
    CELL_C = auto()
    CELL_K = auto()
    CELL_VS = auto()
    CELL_CS = auto()
    CELL_VCVS = auto()
    CELL_CCVS = auto()
    CELL_VCCS = auto()
    CELL_CCCS = auto()
    CELL_DIODE = auto()
    CELL_MOSFET = auto()
    CELL_BJT = auto()
    CELL_JFET = auto()
    CELL_CELL = auto()
    #
    CELL_NMOS = auto()
    CELL_PMOS = auto()
    CELL_NPN = auto()
    CELL_PNP = auto()
    CELL_NJF = auto()
    CELL_PJF = auto()
    #
    CELL_CELL_DIODE = auto()
    CELL_CELL_NMOS = auto()
    CELL_CELL_PMOS = auto()
    CELL_CELL_NPN = auto()
    CELL_CELL_PNP = auto()
    CELL_CELL_NJF = auto()
    CELL_CELL_PJF = auto()
    #
    INST_R = auto()
    INST_L = auto()
    INST_C = auto()
    INST_K = auto()
    INST_VS = auto()
    INST_CS = auto()
    INST_VCVS = auto()
    INST_CCVS = auto()
    INST_VCCS = auto()
    INST_CCCS = auto()
    INST_DIODE = auto()
    INST_MOSFET = auto()
    INST_BJT = auto()
    INST_JFET = auto()
    INST_INST = auto()


class Func(Enum):
    MAKEIPROBE = auto()
    FINDVNET = auto()
    FINDDECAP = auto()


class Const:
    def __init__(self):
        pass

    def get_k_topcell_name(self):
        return "___xxx_top_xxx___"

    def get_k_line_step(self):
        return 1_000_000_000

    def get_k_r_cell_name(self):
        return "r"

    def get_k_l_cell_name(self):
        return "l"

    def get_k_c_cell_name(self):
        return "c"

    def get_k_k_cell_name(self):
        return "k"

    def get_k_vs_cell_name(self):
        return "v"

    def get_k_cs_cell_name(self):
        return "i"

    def get_k_vcvs_cell_name(self):
        return "e"

    def get_k_ccvs_cell_name(self):
        return "g"

    def get_k_vccs_cell_name(self):
        return "h"

    def get_k_cccs_cell_name(self):
        return "f"

    def get_k_cellname_dic():
        k_DEFAULT_CELLNAME_DIC = {
            Type.CELL_R: "r",
            Type.CELL_L: "l",
            Type.CELL_C: "c",
            Type.CELL_K: "k",
            Type.CELL_VS: "v",
            Type.CELL_CS: "i",
            Type.CELL_VCVS: "e",
            Type.CELL_CCVS: "g",
            Type.CELL_VCCS: "h",
            Type.CELL_CCCS: "f",
        }
        return k_DEFAULT_CELLNAME_DIC


class Utils:
    def __init__(self):
        pass

    def get_first_char_inst(self, type):
        k_DEFAULT_FIRST_CHAR_DIC = {
            Type.INST_R: "r",
            Type.INST_L: "l",
            Type.INST_C: "c",
            Type.INST_K: "k",
            Type.INST_VS: "v",
            Type.INST_CS: "i",
            Type.INST_VCVS: "e",
            Type.INST_CCVS: "g",
            Type.INST_VCCS: "h",
            Type.INST_CCCS: "f",
            Type.INST_DIODE: "d",
            Type.INST_MOSFET: "m",
            Type.INST_BJT: "q",
            Type.INST_JFET: "j",
            Type.INST_INST: "x",
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
            Type.CELL_CELL_DIODE,
            Type.CELL_CELL_NMOS,
            Type.CELL_CELL_PMOS,
            Type.CELL_CELL_NPN,
            Type.CELL_CELL_PNP,
            Type.CELL_CELL_NJF,
            Type.CELL_CELL_PJF,
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
            Type.CELL_DIODE,
            Type.CELL_NMOS,
            Type.CELL_PMOS,
            Type.CELL_NPN,
            Type.CELL_PNP,
            Type.CELL_NJF,
            Type.CELL_PJF,
        ]

    def get_type_name(self, type):
        match type:
            case Type.CELL_R:
                return "r"
            case Type.CELL_L:
                return "l"
            case Type.CELL_C:
                return "c"
            case Type.CELL_K:
                return "k"
            case Type.CELL_DIODE:
                return "d"
            case Type.CELL_NMOS:
                return "nmos"
            case Type.CELL_PMOS:
                return "pmos"
            case Type.CELL_NPN:
                return "npn"
            case Type.CELL_PNP:
                return "pnp"
            case Type.CELL_NJF:
                return "njf"
            case Type.CELL_PJF:
                return "pjf"
            case Type.CELL_VS:
                return "vs"
            case Type.CELL_CS:
                return "cs"
            case Type.CELL_VCVS:
                return "vcvs"
            case Type.CELL_CCVS:
                return "ccvs"
            case Type.CELL_VCCS:
                return "vccs"
            case Type.CELL_CCCS:
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
