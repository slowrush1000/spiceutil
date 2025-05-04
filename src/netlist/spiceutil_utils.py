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
    CELL_VS = auto()
    CELL_CS = auto()
    CELL_VCVS = auto()
    CELL_CCVS = auto()
    CELL_VCCS = auto()
    CELL_CCCS = auto()
    CELL_R = auto()
    CELL_C = auto()
    CELL_L = auto()
    CELL_K = auto()
    CELL_DIODE = auto()
    CELL_BJT = auto()
    CELL_BJT_NPN = auto()
    CELL_BJT_PNP = auto()
    CELL_MOSFET = auto()
    CELL_MOSFET_NMOS = auto()
    CELL_MOSFET_PMOS = auto()
    CELL_JFET = auto()
    CELL_JFET_NJF = auto()
    CELL_JFET_PJF = auto()
    #    CELL_CELL_DIODE = auto()
    #    CELL_CELL_BJT = auto()
    #    CELL_CELL_BJT_NPN = auto()
    #    CELL_CELL_BJT_PNP = auto()
    #    CELL_CELL_MOSFET = auto()
    #    CELL_CELL_MOSFET_NMOS = auto()
    #    CELL_CELL_MOSFET_PMOS = auto()
    #    CELL_CELL_JFET = auto()
    #    CELL_CELL_JFET_NJF = auto()
    #    CELL_CELL_JFET_PJF = auto()
    CELL_CELL = auto()
    #
    INST_VS = auto()
    INST_CS = auto()
    INST_VCVS = auto()
    INST_CCVS = auto()
    INST_VCCS = auto()
    INST_CCCS = auto()
    INST_R = auto()
    INST_C = auto()
    INST_L = auto()
    INST_K = auto()
    INST_DIODE = auto()
    INST_BJT = auto()
    INST_MOSFET = auto()
    INST_JFET = auto()
    INST_INST = auto()
    #


def is_cell_model(type):
    cells = [
        Type.CELL_DIODE,
        Type.CELL_BJT,
        Type.CELL_BJT_NPN,
        Type.CELL_BJT_PNP,
        Type.CELL_MOSFET,
        Type.CELL_MOSFET_NMOS,
        Type.CELL_MOSFET_PMOS,
        Type.CELL_JFET,
        Type.CELL_JFET_NJF,
        Type.CELL_JFET_PJF,
    ]
    cell_set = set(cells)
    if type in cell_set:
        return True
    else:
        return False


def k_DEFAULT_TOP_CELL_NAME():
    return "___xxx_top_xxx___"


def k_LINE_STEP():
    return 1_000_000_000


def k_DEFAULT_CELLS():
    return [
        Type.CELL_VS,
        Type.CELL_CS,
        Type.CELL_VCVS,
        Type.CELL_CCVS,
        Type.CELL_VCCS,
        Type.CELL_CCCS,
        Type.CELL_R,
        Type.CELL_C,
        Type.CELL_L,
        Type.CELL_K,
    ]


def k_DEFAULT_CELL_DIC():
    default_cell_dic = {
        Type.CELL_VS: "v",
        Type.CELL_CS: "i",
        Type.CELL_VCVS: "e",
        Type.CELL_VCCS: "g",
        Type.CELL_CCVS: "h",
        Type.CELL_CCCS: "f",
        Type.CELL_R: "r",
        Type.CELL_C: "c",
        Type.CELL_L: "l",
        Type.CELL_K: "k",
    }
    return default_cell_dic


def get_default_cell_name(cell_type):
    if cell_type in k_DEFAULT_CELL_DIC():
        return k_DEFAULT_CELL_DIC()[cell_type]
    else:
        return ""


def is_default_cell(cell_name, cell_type):
    if cell_type in k_DEFAULT_CELL_DIC():
        t_cell_name = k_DEFAULT_CELL_DIC()[cell_type]
        if t_cell_name == cell_name:
            return True
    return False


def get_model_cell_type(model_type_str):
    match (model_type_str):
        case "r":
            return Type.CELL_R
        case "l":
            return Type.CELL_L
        case "c":
            return Type.CELL_C
        case "d":
            return Type.CELL_DIODE
        case "npn":
            return Type.CELL_BJT_NPN
        case "pnp":
            return Type.CELL_BJT_PNP
        case "nmos":
            return Type.CELL_MOSFET_NMOS
        case "pmos":
            return Type.CELL_MOSFET_PMOS
        case "njf":
            return Type.CELL_JFET_NJF
        case "pjf":
            return Type.CELL_JFET_PJF
        case _:
            return Type.INIT


def get_model_cell_name(model_type):
    match (model_type):
        case Type.CELL_R:
            return "r"
        case Type.CELL_C:
            return "c"
        case Type.CELL_L:
            return "l"
        case Type.CELL_DIODE:
            return "d"
        case Type.CELL_BJT_NPN:
            return "npn"
        case Type.CELL_BJT_PNP:
            return "pnp"
        case Type.CELL_MOSFET_NMOS:
            return "nmos"
        case Type.CELL_MOSFET_PMOS:
            return "pmos"
        case Type.CELL_JFET_NJF:
            return "njf"
        case Type.CELL_JFET_PJF:
            return "pjf"
        case _:
            return "*"


def k_SUBCKT_MODEL_SET():
    subckt_model_set = (
        Type.CELL_DIODE,
        Type.CELL_BJT,
        Type.CELL_BJT_NPN,
        Type.CELL_BJT_PNP,
        Type.CELL_MOSFET,
        Type.CELL_MOSFET_NMOS,
        Type.CELL_MOSFET_PMOS,
        Type.CELL_JFET,
        Type.CELL_JFET_NJF,
        Type.CELL_JFET_PJF,
    )
    return subckt_model_set


def get_file_func_line_s(msg):
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    return f"{msg}({os.path.basename(filename)}:{function_name}:{line_number})"


def write_wrap_line(file, line, textwidth=100):
    wrap_lines = textwrap.wrap(
        line,
        width=textwidth,
        subsequent_indent="+ ",
        break_long_words=False,
        break_on_hyphens=False,
    )
    for wrap_line in wrap_lines:
        file.write(f"{wrap_line}")


#
#
# class Run(Enum):
#    INIT = auto()
#    MAKEIPROBE = auto()
#    FINDVNET = auto()
#    FINDDECAP = auto()
#
#
#
#
#
# def get_k_default_cellname_r():
#    return "r"
#
#
# def get_k_default_cellname_l():
#    return "l"
#
#
# def get_k_default_cellname_c():
#    return "c"
#
#
# def get_k_default_cellname_k():
#    return "k"
#
#
# def get_k_default_cellname_vs():
#    return "v"
#
#
# def get_k_default_cellname_cs():
#    return "i"
#
#
# def get_k_default_cellname_vcvs():
#    return "e"
#
#
# def get_k_default_cellname_ccvs():
#    return "g"
#
#
# def get_k_default_cellname_vccs():
#    return "h"
#
#
# def get_k_default_cellname_cccs():
#    return "f"
#
#
# def get_k_default_cellname_dic():
#    k_DEFAULT_CELLNAME_DIC = {
#        Type.CELL_R: "r",
#        Type.CELL_L: "l",
#        Type.CELL_C: "c",
#        Type.CELL_K: "k",
#        Type.CELL_VS: "v",
#        Type.CELL_CS: "i",
#        Type.CELL_VCVS: "e",
#        Type.CELL_CCVS: "g",
#        Type.CELL_VCCS: "h",
#        Type.CELL_CCCS: "f",
#    }
#    return k_DEFAULT_CELLNAME_DIC
#
#
# def get_first_char_inst(type):
#    k_DEFAULT_FIRST_CHAR_DIC = {
#        Type.INST_R: "r",
#        Type.INST_L: "l",
#        Type.INST_C: "c",
#        Type.INST_K: "k",
#        Type.INST_VS: "v",
#        Type.INST_CS: "i",
#        Type.INST_VCVS: "e",
#        Type.INST_CCVS: "g",
#        Type.INST_VCCS: "h",
#        Type.INST_CCCS: "f",
#        Type.INST_DIODE: "d",
#        Type.INST_MOSFET: "m",
#        Type.INST_BJT: "q",
#        Type.INST_JFET: "j",
#        Type.INST_INST: "x",
#    }
#    if type in k_DEFAULT_FIRST_CHAR_DIC:
#        return k_DEFAULT_FIRST_CHAR_DIC[type]
#    else:
#        return "*"
#
#
# def get_k_default_cellname_set():
#    k_DEFAULT_CELLLNAMES = ["r", "l", "c", "k", "v", "i", "e", "g", "h", "f"]
#    k_DEFAULT_CELLNAME_SET = set(k_DEFAULT_CELLLNAMES)
#    return k_DEFAULT_CELLNAME_SET
#
#
# def get_subckt_types_set():
#    k_SUBCKT_TYPES = [
#        Type.CELL_CELL_DIODE,
#        Type.CELL_CELL_NMOS,
#        Type.CELL_CELL_PMOS,
#        Type.CELL_CELL_NPN,
#        Type.CELL_CELL_PNP,
#        Type.CELL_CELL_NJF,
#        Type.CELL_CELL_PJF,
#    ]
#    k_SUBCKT_TYPES_SET = set(k_SUBCKT_TYPES)
#    return k_SUBCKT_TYPES_SET
#
#
# def is_subckt_type(type):
#    # subckt_types = get_subckt_types()
#    # subckt_types_set = set(k_SUBCKT_TYPES)
#    if type in get_subckt_types_set():
#        return True
#    else:
#        return False
#
#
# def get_device_types():
#    return [
#        Type.CELL_DIODE,
#        Type.CELL_NMOS,
#        Type.CELL_PMOS,
#        Type.CELL_NPN,
#        Type.CELL_PNP,
#        Type.CELL_NJF,
#        Type.CELL_PJF,
#    ]
#
#
# def get_type_name(type):
#    match type:
#        case Type.CELL_R:
#            return "r"
#        case Type.CELL_L:
#            return "l"
#        case Type.CELL_C:
#            return "c"
#        case Type.CELL_K:
#            return "k"
#        case Type.CELL_DIODE:
#            return "d"
#        case Type.CELL_NMOS:
#            return "nmos"
#        case Type.CELL_PMOS:
#            return "pmos"
#        case Type.CELL_NPN:
#            return "npn"
#        case Type.CELL_PNP:
#            return "pnp"
#        case Type.CELL_NJF:
#            return "njf"
#        case Type.CELL_PJF:
#            return "pjf"
#        case Type.CELL_VS:
#            return "vs"
#        case Type.CELL_CS:
#            return "cs"
#        case Type.CELL_VCVS:
#            return "vcvs"
#        case Type.CELL_CCVS:
#            return "ccvs"
#        case Type.CELL_VCCS:
#            return "vccs"
#        case Type.CELL_CCCS:
#            return "cccs"
#        case _:
#            return ""
#
#
# def get_error_str(msg):
#    frame = inspect.currentframe().f_back
#    filename = frame.f_code.co_filename
#    function_name = frame.f_code.co_name
#    line_number = frame.f_lineno
#    return f"{msg}({os.path.basename(filename)}:{function_name}:{line_number})"
#
#
# def get_netname(hier_netname):
#    return hier_netname.split(".")[-1]
#
#
#
