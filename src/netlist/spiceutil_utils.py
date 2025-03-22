from enum import Enum, auto
import inspect


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
    CELL_DIODE = auto()
    CELL_MOSFET = auto()
    CELL_BJT = auto()
    CELL_JFET = auto()
    CELL_VS = auto()
    CELL_CS = auto()
    CELL_VCVS = auto()
    CELL_CCVS = auto()
    CELL_VCCS = auto()
    CELL_CCCS = auto()
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
    INST_DIODE = auto()
    INST_MOSFET = auto()
    INST_BJT = auto()
    INST_JFET = auto()
    INST_VS = auto()
    INST_CS = auto()
    INST_VCVS = auto()
    INST_CCVS = auto()
    INST_VCCS = auto()
    INST_CCCS = auto()
    INST_INST = auto()


class Run(Enum):
    INIT = auto()
    MAKEIPROBE = auto()
    FINDVNET = auto()
    FINDDECAP = auto()


k_TOP_CELLNAME = "___xxx_top_xxx__"
k_LINE_STEP = 1_000_000
k_DEFAULT_R_CELL = "r"
k_DEFAULT_L_CELL = "l"
k_DEFAULT_C_CELL = "c"


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


def is_subckt_type(type):
    # subckt_types = get_subckt_types()
    # subckt_types_set = set(k_SUBCKT_TYPES)
    if type in k_SUBCKT_TYPES_SET:
        return True
    else:
        return False


def get_device_types():
    return [
        Type.CELL_DIODE,
        Type.CELL_NMOS,
        Type.CELL_PMOS,
        Type.CELL_NPN,
        Type.CELL_PNP,
        Type.CELL_NJF,
        Type.CELL_PJF,
    ]


def get_type_name(type):
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


def get_trace_info_str():
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    return f"{filename} : {function_name} : {line_number}"


def get_error_str(msg):
    return f"{msg}({get_trace_info_str()})"


def get_netname(hier_netname):
    return hier_netname.split(".")[-1]
