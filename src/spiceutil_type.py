
from enum import Enum

class Type(Enum):
    INIT        = 0
    #
    NODE_PIN    = 1
    NODE_NODE   = 2
    #
    CELL_R      = 3
    CELL_L      = 4
    CELL_C      = 5
    CELL_MOSFET = 6
    CELL_BJT    = 7
    CELL_DIODE  = 8
    CELL_CELL   = 9
    #
    INST_R      = 10
    INST_L      = 11
    INST_C      = 12
    INST_MOSFET = 13
    INST_BJT    = 14
    INST_DIODE  = 15
    INST_INST   = 16