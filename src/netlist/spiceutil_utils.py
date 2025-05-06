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


class Runmode(Enum):
    INIT = auto()
    #
    CONFIG = auto()
    PARSER = auto()
    FINDVNET = auto()
    MAKEIPROBE = auto()
    FLATTEN = auto()


def k_RUNMODE_DIC():
    runmode_dic = {
        "config": Runmode.CONFIG,
        "parser": Runmode.PARSER,
        "findvnet": Runmode.FINDVNET,
        "makeiprobe": Runmode.MAKEIPROBE,
        "flatten": Runmode.FLATTEN,
    }
    return runmode_dic


def get_runmode(runmode_s):
    if runmode_s in k_RUNMODE_DIC():
        return k_RUNMODE_DIC()[runmode_s]
    else:
        return Runmode.INIT


def get_runmode_keys():
    keys = k_RUNMODE_DIC().keys()
    return " ".join(keys)


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


def get_inst_type_cell_type(first_char):
    k_first_char_type_dic = {
        "r": [Type.INST_R, Type.CELL_R],
        "c": [Type.INST_C, Type.CELL_C],
        "l": [Type.INST_L, Type.CELL_L],
        "k": [Type.INST_K, Type.CELL_K],
        "v": [Type.INST_VS, Type.CELL_VS],
        "i": [Type.INST_CS, Type.CELL_CS],
        "e": [Type.INST_VCVS, Type.CELL_VCVS],
        "g": [Type.INST_VCCS, Type.CELL_VCCS],
        "h": [Type.INST_CCVS, Type.CELL_CCVS],
        "f": [Type.INST_CCCS, Type.CELL_CCCS],
        "d": [Type.INST_DIODE, Type.CELL_DIODE],
        "j": [Type.INST_JFET, Type.CELL_JFET],
        "q": [Type.INST_BJT, Type.CELL_BJT],
        "m": [Type.INST_MOSFET, Type.CELL_MOSFET],
    }
    if first_char in k_first_char_type_dic:
        return k_first_char_type_dic[first_char][0], k_first_char_type_dic[first_char][1]
    else:
        return Type.INIT, Type.INIT
    # return inst_type, cell_type
    #    if "r" == first_char:
    #        inst_type = Type.INST_R
    #        cell_type = Type.CELL_R
    #    elif "l" == first_char:
    #        inst_type = Type.INST_L
    #        cell_type = Type.CELL_L
    #    elif "c" == first_char:
    #        inst_type = Type.INST_C
    #        cell_type = Type.CELL_C
    #    elif "k" == first_char:
    #        inst_type = Type.INST_K
    #        cell_type = Type.CELL_K
    #    elif "v" == first_char:
    #        inst_type = Type.INST_VS
    #        cell_type = Type.CELL_VS
    #    elif "i" == first_char:
    #        inst_type = Type.INST_CS
    #        cell_type = Type.CELL_CS
    #    elif "e" == first_char:
    #        inst_type = Type.INST_VCVS
    #        cell_type = Type.CELL_VCVS
    #    elif "g" == first_char:
    #        inst_type = Type.INST_VCCS
    #        cell_type = Type.CELL_VCCS
    #    elif "h" == first_char:
    #        inst_type = Type.INST_CCVS
    #        cell_type = Type.CELL_CCVS
    #    elif "f" == first_char:
    #        inst_type = Type.INST_CCCS
    #        cell_type = Type.CELL_CCCS
    #    elif "d" == first_char:
    #        inst_type = Type.INST_DIODE
    #        cell_type = Type.CELL_DIODE
    #    elif "j" == first_char:
    #        inst_type = Type.INST_JFET
    #        cell_type = Type.CELL_JFET
    #    elif "q" == first_char:
    #        inst_type = Type.INST_BJT
    #        cell_type = Type.CELL_BJT
    #    elif "m" == first_char:
    #        inst_type = Type.INST_MOSFET
    #        cell_type = Type.CELL_MOSFET
    #    else:
    #        inst_type = Type.INIT
    #        cell_type = Type.INIT
    # return inst_type, cell_type


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


# x0.x1.x2.x3 -> x0, x1, x2, x3
def get_net_name(hier_netname):
    return hier_netname.split(".")[-1]
    #


def get_cell_key(name, type, delim="="):
    return f"{name}{delim}{type.name}"


def split_cell_key(cell_key, delim="="):
    tokens = cell_key.split(delim)
    cell_name = tokens[0]
    cell_type = Type[tokens[1].strip()]
    return cell_name, cell_type


def is_equal(s1, s2, casesensitive=True):
    if True == casesensitive:
        if s1 == s2:
            return True
        else:
            return False
    else:
        if s1.lower() == s2.lower():
            return True
        else:
            return False
