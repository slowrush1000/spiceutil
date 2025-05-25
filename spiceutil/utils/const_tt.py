from .type_tt import Type_tt


class Const:
    def __init__(self):
        pass

    def get_topcell_name(self):
        return "___xxx_top_xxx___"

    def get_line_step(self):
        return 1_000_000_000

    def get_r_cell_name(self):
        return "r"

    def get_l_cell_name(self):
        return "l"

    def get_c_cell_name(self):
        return "c"

    def get_k_cell_name(self):
        return "k"

    def get_vs_cell_name(self):
        return "v"

    def get_cs_cell_name(self):
        return "i"

    def get_vcvs_cell_name(self):
        return "e"

    def get_ccvs_cell_name(self):
        return "g"

    def get_vccs_cell_name(self):
        return "h"

    def get_cccs_cell_name(self):
        return "f"

    def get_cellname_dic(self):
        k_DEFAULT_CELLNAME_DIC = {
            Type_tt.CELL_R: "r",
            Type_tt.CELL_L: "l",
            Type_tt.CELL_C: "c",
            Type_tt.CELL_K: "k",
            Type_tt.CELL_VS: "v",
            Type_tt.CELL_CS: "i",
            Type_tt.CELL_VCVS: "e",
            Type_tt.CELL_CCVS: "g",
            Type_tt.CELL_VCCS: "h",
            Type_tt.CELL_CCCS: "f",
        }
        return k_DEFAULT_CELLNAME_DIC
