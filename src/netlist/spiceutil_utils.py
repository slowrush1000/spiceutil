#
from enum import Enum
#
class Version:
    def __init__(self):
        self.m_program  = 'spiceutil'
        self.m_version  = '20250119.0.0'
#
def k_TOP_CELLNAME():
    return '___xxx_top_xxx___'
def k_LINE_STEP():
    return 1_000_000
def GetDefaultRCell():
    return 'r'
def GetDefaultLCell():
    return 'l'
def GetDefaultCCell():
    return 'c'
def GetProgram():
    my_version  = Version()
    return my_version.m_program
def GetVersion():
    my_version  = Version()
    return my_version.m_version
#
class Type(Enum):
    INIT            = 0
    #
    NODE_PIN        = 1
    NODE_NODE       = 2
    #
    CELL_R          = 10
    CELL_L          = 11
    CELL_C          = 12
    CELL_DIODE      = 14
    CELL_MOSFET     = 15
    CELL_BJT        = 16
    CELL_JFET       = 17
    CELL_CELL       = 18
    #
    CELL_NMOS       = 20
    CELL_PMOS       = 21
    CELL_NPN        = 22
    CELL_PNP        = 23
    CELL_NJF        = 24
    CELL_PJF        = 25
    #
    CELL_DIODE_S    = 30
    CELL_NMOS_S     = 31
    CELL_PMOS_S     = 32
    CELL_NPN_S      = 33
    CELL_PNP_S      = 34
    CELL_NJF_S      = 35
    CELL_PJF_S      = 36
    #
    INST_R          = 50
    INST_L          = 51
    INST_C          = 52
    INST_DIODE      = 53
    INST_MOSFET     = 54
    INST_BJT        = 55
    INST_JFET       = 56
    INST_INST       = 57
#
def GetTypeName(type):
    match type:
        case Type.CELL_R:
            return 'r'
        case Type.CELL_L:
            return 'l'
        case Type.CELL_C:
            return 'c'
        case Type.CELL_DIODE:
            return 'd'
        case Type.CELL_NMOS:
            return 'nmos'
        case Type.CELL_PMOS:
            return 'pmos'
        case Type.CELL_NPN:
            return 'npn'
        case Type.CELL_PNP:
            return 'pnp'
        case Type.CELL_NJF:
            return 'njf'
        case Type.CELL_PJF:
            return  'pjf'
        case _:
            return ''
#
class Run(Enum):
    MAKEIPROBE      =   0