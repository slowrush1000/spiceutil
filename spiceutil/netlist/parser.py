import sys
import os
import inspect
import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from netlist.cell import Cell
from netlist.inst import Inst
from netlist.netlist import Netlist
from netlist.node import Node
from netlist.object import Object
from netlist.parameters import Parameters
from utils import Utils
from utils import Const
from utils import Type_tt
from version import Version
from performance import Performance
from write import Write


class Parser:
    def __init__(self, t_input=None, t_netlist=None, t_log=None):
        self.__input = t_input
        self.__netlist = t_netlist
        self.__log = t_log
        #
        self.__curcell_name = Const().get_topcell_name()
        self.__curcell = None
        self.__default_topcell = self.get_netlist().get_cell(
            Const().get_topcell_name(), Type_tt.CELL_CELL
        )
        if None == self.__default_topcell:
            self.__default_topcell = Cell(Const().get_topcell_name(), Type_tt.CELL_CELL)
            self.__netlist.add_cell(
                Const().get_topcell_name(),
                self.__default_topcell,
                Type_tt.CELL_CELL,
            )

    def set_input(self, input):
        self.__input = input

    def get_input(self):
        return self.__input

    def set_netlist(self, netlist):
        self.__netlist = netlist

    def get_netlist(self):
        return self.__netlist

    def set_log(self, log):
        self.__log = log

    def get_log(self):
        return self.__log

    def set_curcell_name(self, cellname):
        self.__curcell_name = cellname

    def get_curcell_name(self):
        return self.__curcell_name

    def set_curcell(self, cell):
        self.__curcell = cell

    def get_curcell(self):
        return self.__curcell

    def get_default_topcell(self):
        return self.__default_topcell

    def init_cell(self):
        self.get_log().get_logger().info(f"# init cell start")
        for type in Const().get_cellname_dic():
            name = Const().get_cellname_dic()[type]
            cell = Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)
        self.get_log().get_logger().info(f"# init cell end")

    def read_1st(self, filename):
        self.get_log().get_logger().info(
            f"# read file({filename}) 1st start ... {
            datetime.datetime.now()}"
        )
        nlines = 0
        total_line = ""
        try:
            with open(filename, "rt") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    nlines = nlines + 1
                    if 0 == (nlines % Const().get_line_step()):
                        self.get_log().get_logger().info(
                            f"    {nlines} lines ... {
                                datetime.datetime.now()}"
                        )
                    #
                    if False == self.get_input().get_case_sense():
                        line = line.lower()
                    line = line.lstrip().rstrip()
                    line = self.remove_comments(line, self.get_input().get_dollar_comment())
                    if 0 == len(line):
                        continue
                    #
                    if "+" == line[0]:
                        total_line = total_line + line[1:]
                    else:
                        self.read_total_line_1st(total_line, filename)
                    total_line = line
        except FileNotFoundError:
            self.get_log().get_logger().error(f"# error: file{filename} open failed.")
            self.__log.get_logger().info(
                f"# spiceutil({Version().get_program_version()}) end ... {datetime.datetime.now()}\n"
            )
            exit()
        self.read_total_line_1st(total_line, filename)
        self.get_log().get_logger().info(
            f"    {nlines} lines ... {
            datetime.datetime.now()}"
        )
        self.get_log().get_logger().info(
            f"# read file({filename}) 1st end ... {datetime.datetime.now()}\n"
        )

    def read_total_line_1st(self, total_line, filename):
        t_total_line = total_line.replace("=", " = ")
        tokens = t_total_line.split()
        if 0 == len(tokens):
            return
        if ".subckt" == tokens[0].lower():
            self.read_total_line_1st_subckt_line(tokens)
        elif ".end" == tokens[0].lower():
            self.read_total_line_1st_ends_line(tokens)
        elif ".model" == tokens[0].lower():
            self.read_total_line_1st_model_line(tokens)
        elif (".inc" == tokens[0].lower()) or (".include" == tokens[0].lower()):
            self.read_total_line_1st_include_line(tokens, filename)

    def read_total_line_1st_subckt_line(self, tokens):
        name = tokens[1]
        type = Type_tt.CELL_CELL
        key = self.get_netlist().get_cell_key(name, type)
        cell = self.get_netlist().get_cell_by_key(key)
        if None == cell:
            cell = Cell(name, type)
            self.set_curcell_name(name)
            self.get_netlist().add_cell(name, cell, type)
            self.get_netlist().add_key(key)

    def read_total_line_1st_ends_line(self):
        self.set_curcell_name(Const().get_topcell_name())
        self.set_curcell(self.get_default_topcell())

    # .model name ...
    def read_total_line_1st_model_line(self, tokens):
        name = tokens[1].split(".")[0]
        type_name = tokens[2]
        type = Type_tt.INIT
        if "d" == type_name:
            type = Type_tt.CELL_DIODE
        elif "npn" == type_name:
            type = Type_tt.CELL_NPN
        elif "pnp" == type_name:
            type = Type_tt.CELL_PNP
        elif "nmos" == type_name:
            type = Type_tt.CELL_NMOS
        elif "pmos" == type_name:
            type = Type_tt.CELL_PMOS
        elif "njf" == type_name:
            type = Type_tt.CELL_NJF
        elif "pjf" == type_name:
            type = Type_tt.CELL_PJF
        #
        cell = self.get_netlist().get_cell(name, type)
        if None == cell:
            cell = Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)
        #
        self.read_parameter_cell(cell, tokens, 2)

    def read_total_line_1st_include_line(self, tokens, filename):
        t_filename = tokens[1].replace('"', "").replace("'", "")
        # 절대경로
        if "/" == t_filename[0]:
            self.read_1st(t_filename)
        # 상대경로
        else:
            absfilename = os.path.abspath(filename)
            absdirname = os.path.dirname(absfilename)
            t_filename = f"{absdirname}/{t_filename}"
            self.read_1st(t_filename)

    def read_2nd(self, filename):
        self.get_log().get_logger().info(
            f"# read file({filename}) 2nd start ... {
            datetime.datetime.now()}"
        )
        nlines = 0
        total_line = ""
        with open(filename, "rt") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                nlines = nlines + 1
                if 0 == (nlines % Const().get_line_step()):
                    self.get_log().get_logger().info(
                        f"    {nlines} lines ... {
                        datetime.datetime.now()}"
                    )
                #
                if False == self.get_input().get_case_sense():
                    line = line.lower()
                line = line.lstrip().rstrip()
                line = self.remove_comments(line, self.get_input().get_dollar_comment())
                if 0 == len(line):
                    continue
                #
                if "+" == line[0]:
                    total_line = total_line + line[1:]
                else:
                    self.read_total_line_2nd(total_line, filename)
                    total_line = line
        self.read_total_line_2nd(total_line, filename)
        self.get_log().get_logger().info(
            f"    {nlines} lines ... {
            datetime.datetime.now()}"
        )
        self.get_log().get_logger().info(
            f"# read file({filename}) 2nd end ... {datetime.datetime.now()}\n"
        )

    def read_total_line_2nd(self, total_line, filename):
        t_total_line = total_line.replace("=", " = ")
        tokens = t_total_line.split()
        if 0 == len(tokens):
            return
        if ".subckt" == tokens[0].lower():
            self.read_total_line_2nd_subckt_line(tokens)
        elif ".ends" == tokens[0].lower():
            self.read_total_line_1st_ends_line()
        elif ".model" == tokens[0].lower():
            pass
        elif ".global" == tokens[0].lower():
            self.read_total_line_2nd_global_line(tokens)
        elif ".inc" == tokens[0] or ".include" == tokens[0]:
            self.read_total_line_2dn_include_line(tokens, filename)
        elif Const().get_r_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_r_line(tokens)
        elif Const().get_c_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_c_line(tokens)
        elif Const().get_l_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_l_line(tokens)
        elif Const().get_k_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_line(tokens)
        elif Const().get_vs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_vs_line(tokens)
        elif Const().get_cs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_cs_line(tokens)
        elif Const().get_vcvs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_vcvs_line(tokens)
        elif Const().get_ccvs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_ccvs_line(tokens)
        elif Const().get_vccs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_vccs_line(tokens)
        elif Const().get_cccs_cell_name() == tokens[0][0]:
            self.read_total_line_2nd_cccs_line(tokens)
        elif "m" == tokens[0][0]:
            self.read_total_line_2nd_mosfet_line(tokens)
        elif "q" == tokens[0][0]:
            self.read_total_line_2nd_bjt_line(tokens)
        elif "j" == tokens[0][0]:
            self.read_total_line_2nd_jfet_line(tokens)
        elif "d" == tokens[0][0]:
            self.read_total_line_2nd_diode_line(tokens)
        elif "x" == tokens[0][0]:
            self.read_total_line_2nd_inst_line(tokens)

    def read_total_line_2nd_subckt_line(self, tokens):
        cell_name = tokens[1]
        cell_type = Type_tt.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in Utils().get_subckt_types_set():
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
        if None == cell:
            msg = f"cell({cell_name}) dont exist!"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        self.set_curcell(cell)
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        if -1 == parameter_start_pos:
            parameter_start_pos = len(tokens)
        for pos in range(2, parameter_start_pos):
            # self.get_log().get_logger().debug(f'{cell_name} - {tokens[pos]}')
            pin_name = tokens[pos]
            if None == cell.get_node(pin_name):
                # if False == cell.is_exist_node(pin_name):
                # self.get_log().get_logger().debug(f'{cell_name} - {pin_name}')
                pin = Node(pin_name, Type_tt.NODE_PIN)
                cell.add_pin(pin_name, pin)
            else:
                msg = f"# error : cell({cell_name}) pin({pin_name}) is duplicate!"
                self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
                exit()
        #
        cell.make_pin_set()
        #
        self.read_parameter_cell(cell, tokens, parameter_start_pos)

    # .global netnames...
    def read_total_line_2nd_global_line(self, tokens):
        for token in tokens[1:]:
            self.get_netlist().add_global_netname(token)
        self.get_netlist().make_global_netnames_set()

    def read_total_line_2dn_include_line(self, tokens, filename):
        t_filename = tokens[1].replace('"', "").replace("'", "")
        # 절대경로
        if "/" == t_filename[0]:
            self.read_1st(t_filename)
        # 상대경로
        else:
            absfilename = os.path.abspath(filename)
            absdirname = os.path.dirname(absfilename)
            t_filename = f"{absdirname}/{t_filename}"
            self.read_2nd(t_filename)

    def read_total_line_2nd_r_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_R)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = Const().get_r_cell_name()
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        # self.get_log().get_logger().debug(f'debug- {cell_name}')
        # rname n1 n2 value
        cell_type = Type_tt.CELL_R
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        # rname n1 n2 value
        else:
            parameter_name = Const().get_r_cell_name()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # cname n1 n2 value

    def read_total_line_2nd_c_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_C)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = Const().get_c_cell_name()
        # cname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        cell_type = Type_tt.CELL_C
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        else:
            parameter_name = Const().get_c_cell_name()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # lname n1 n2 value

    def read_total_line_2nd_l_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_L)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            if 0 == len(inst.get_nodes()):
                inst = Inst(inst_name, Type_tt.INST_L)
                self.get_curcell().add_inst(inst_name, inst)
            else:
                msg = f"# error : inductor({inst_name}) is duplicate in cell({self.get_curcell_name()})"
                self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
                exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = Const().get_l_cell_name()
        # lname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        cell_type = Type_tt.CELL_L
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        else:
            parameter_name = Const().get_l_cell_name()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # kname inductor1 inductor2 value

    def read_total_line_2nd_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_K)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_k_cell_name()
        cell_type = Type_tt.CELL_K
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            inductor_name = tokens[pos]
            inductor = self.get_curcell().get_inst(inductor_name)
            if None == inductor:
                inductor = Inst(inst_name, Type_tt.INST_L)
                self.get_curcell().add_inst(inductor_name, inductor)
            inst.add_inst(inductor)
        #
        parameter_name = Const().get_k_cell_name()
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # vname n1 n2 value

    def read_total_line_2nd_vs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_VS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_vs_cell_name()
        cell_type = Type_tt.CELL_VS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = "dc"
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # iname n1 n2 value

    def read_total_line_2nd_cs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_CS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_k_cell_name()
        cell_type = Type_tt.CELL_K
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = "dc"
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # ename n1 n2 nc1 nc2 value

    def read_total_line_2nd_vcvs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_VCVS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_vcvs_cell_name()
        cell_type = Type_tt.CELL_VCVS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = Const().get_vcvs_cell_name()
        parameter_equation = tokens[5]
        inst.add_parameter(parameter_name, parameter_equation)

    # gname n1 n2 nc1 nc2 value

    def read_total_line_2nd_ccvs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_CCVS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_ccvs_cell_name()
        cell_type = Type_tt.CELL_CCVS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = Const().get_ccvs_cell_name()
        parameter_equation = tokens[5]
        inst.add_parameter(parameter_name, parameter_equation)

    # hname n1 n2 vcontrol value

    def read_total_line_2nd_vccs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_VCCS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_vccs_cell_name()
        cell_type = Type_tt.CELL_VCCS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        vcontrol_name = tokens[3]
        vcontrol = self.get_curcell().get_inst(vcontrol_name)
        if None == vcontrol:
            vcontrol = Inst(vcontrol_name, Type_tt.INST_VS)
            self.get_curcell().add_inst(vcontrol_name, vcontrol)
        inst.add_inst(vcontrol)
        #
        parameter_name = Const().get_vccs_cell_name()
        parameter_equation = tokens[4]
        inst.add_parameter(parameter_name, parameter_equation)

    # fname n1 n2 vcontrol value

    def read_total_line_2nd_cccs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_CCCS)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        cell_name = Const().get_cccs_cell_name()
        cell_type = Type_tt.CELL_CCCS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
        #
        vcontrol_name = tokens[3]
        vcontrol = self.get_curcell().get_inst(vcontrol_name)
        if None == vcontrol:
            vcontrol = Inst(vcontrol_name, Type_tt.INST_VS)
            self.get_curcell().add_inst(vcontrol_name, vcontrol)
        inst.add_inst(vcontrol)
        #
        parameter_name = Const().get_cccs_cell_name()
        parameter_equation = tokens[4]
        inst.add_parameter(parameter_name, parameter_equation)

    # mname n1 n2 n3 n4 cellname l = 100u w = 200u

    def read_total_line_2nd_mosfet_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_MOSFET)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 6
        cell_name = tokens[5].lower()
        cell_type = Type_tt.CELL_NMOS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = Type_tt.CELL_PMOS
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = Type_tt.CELL_MOSFET
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = Type_tt.CELL_MOSFET
                    cell = Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # qname n1 n2 n3 model ...

    def read_total_line_2nd_bjt_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_BJT)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 5
        cell_name = tokens[4].lower()
        cell_type = Type_tt.CELL_NPN
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = Type_tt.CELL_PNP
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = Type_tt.CELL_BJT
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = Type_tt.CELL_BJT
                    cell = Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 4):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # jname n1 n2 n3 model ...

    def read_total_line_2nd_jfet_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_JFET)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 5
        cell_name = tokens[4].lower()
        cell_type = Type_tt.CELL_JFET
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = Type_tt.CELL_PJF
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = Type_tt.CELL_NJF
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = Type_tt.CELL_JFET
                    cell = Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 4):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # dname n1 n2 model ...

    def read_total_line_2nd_diode_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_curcell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_DIODE)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 4
        cell_name = tokens[3].lower()
        cell_type = Type_tt.CELL_DIODE
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # xname n1 n2 ... cell ...

    def read_total_line_2nd_inst_line(self, tokens):
        inst_name = tokens[0]
        cur_cell = self.get_curcell()
        inst = cur_cell.get_inst(inst_name)
        # inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = Inst(inst_name, Type_tt.INST_INST)
            self.get_curcell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_curcell_name()})"
            self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = tokens[parameter_start_pos - 1].lower()
        cell_type = Type_tt.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in Utils().get_subckt_types_set():
                # for cell_type in netlist.SUBCKT_TYPES:
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
            if None == cell:
                self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
                exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = tokens[parameter_start_pos - 1].lower()
        cell_type = Type_tt.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in Utils().get_subckt_types_set():
                # for cell_type in netlist.SUBCKT_TYPES:
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
            if None == cell:
                msg = f"# error : inst({inst_name}) cell({cell_name}) isnot exist!"
                self.get_log().get_logger().error(f"{Utils().get_error_str(msg)}")
            # cell_type = utils.Type.CELL_CELL
            # cell = self.get_netlist().get_cell(cell_name, cell_type)
            # cell = Cell(cell_name, cell_type)
            # self.get_netlist().add_cell(cell_name, cell, cell_type)
        #
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, parameter_start_pos - 1):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
            # cell_type = utils.Type.CELL_CELL
            # cell = self.get_netlist().get_cell(cell_name, cell_type)
            # cell = Cell(cell_name, cell_type)
            # self.get_netlist().add_cell(cell_name, cell, cell_type)
        #
        inst.set_cell(cell)
        # cell.increase_inst_size()
        #
        for pos in range(1, parameter_start_pos - 1):
            node_name = tokens[pos]
            node = self.get_curcell().get_node(node_name)
            if None == node:
                node = Node(node_name, Type_tt.NODE_NODE)
                self.get_curcell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    def read_parameter_start_pos(self, tokens):
        parameter_start_pos = len(tokens)
        for pos in range(1, len(tokens)):
            if "=" == tokens[pos]:
                parameter_start_pos = pos - 1
                break
        return parameter_start_pos

    # *...
    # $...
    # ... name='equation*equation" * comments

    def remove_comments(self, line, dollar_comment=True):
        t_line = line
        t_line = t_line.replace('"', "'")
        # print(f'001 {t_line}')
        # $
        if True == dollar_comment:
            dollar_pos = t_line.find("$")
            if -1 != dollar_pos:
                t_line = t_line[:dollar_pos]
        # print(f'002 {t_line}')
        # *
        quatation_pos = t_line.rfind("'")
        # print(f'003 {quatation_pos}')
        if -1 == quatation_pos:
            star_pos = t_line.find("*")
            # print(f'004 {star_pos}')
            if -1 == star_pos:
                return t_line
            else:
                return t_line[:star_pos]
        else:
            star_pos = t_line.find("*", quatation_pos)
            # print(f'005 {star_pos}')
            if -1 == star_pos:
                return t_line
            else:
                return t_line[:star_pos]

    def read_parameter_cell(self, cell, tokens, parameter_start_pos):
        name_pos = parameter_start_pos
        equation_end_pos = len(tokens)
        for pos in range(len(tokens) - 1, parameter_start_pos, -1):
            if "=" == tokens[pos]:
                name_pos = pos - 1
                equation_start_pos = pos + 1
                # self.get_log().get_logger().debug(f'debug : pos : {pos} name_pos : {name_pos} equation_start_pos : {equation_start_pos} equation_end_pos : {equation_end_pos}')
                name = tokens[name_pos]
                equation = " ".join(tokens[equation_start_pos:equation_end_pos])
                equation = (
                    equation.replace(" ", "").replace("\t", "").replace("'", "").replace('"', "")
                )
                cell.add_parameter(name, equation)
                equation_end_pos = name_pos

    def read_parameter_inst(self, inst, tokens, parameter_start_pos):
        name_pos = parameter_start_pos
        equation_start_pos = len(tokens)
        equation_end_pos = len(tokens)
        for pos in range(len(tokens) - 1, parameter_start_pos, -1):
            if "=" == tokens[pos]:
                name_pos = pos - 1
                equation_start_pos = pos + 1
                name = tokens[name_pos]
                equation = " ".join(tokens[equation_start_pos:equation_end_pos])
                equation = (
                    equation.replace(" ", "").replace("\t", "").replace("'", "").replace('"', "")
                )
                inst.add_parameter(name, equation)
                equation_end_pos = name_pos

    def get_subckt_type(self, type):
        match type:
            case Type_tt.CELL_DIODE:
                return Type_tt.CELL_CELL_DIODE
            case Type_tt.CELL_NMOS:
                return Type_tt.CELL_CELL_NMOS
            case Type_tt.CELL_PMOS:
                return Type_tt.CELL_CELL_PMOS
            case Type_tt.CELL_NPN:
                return Type_tt.CELL_CELL_NPN
            case Type_tt.CELL_PNP:
                return Type_tt.CELL_CELL_PNP
            case Type_tt.CELL_NJF:
                return Type_tt.CELL_CELL_NJF
            case Type_tt.CELL_PJF:
                return Type_tt.CELL_CELL_PJF
            case _:
                return Type_tt.INIT

    def find_subckt_model(self):
        self.get_log().get_logger().info(
            f"# find subckt model start ... {datetime.datetime.now()}"
        )
        #
        insert_name_cell_types = []
        delete_cell_keys = []
        for key in self.get_netlist().get_cell_dic():
            cell = self.get_netlist().get_cell_by_key(key)
            if Type_tt.CELL_CELL == cell.get_type():
                key_0 = self.get_netlist().get_cell_key(cell.get_name(), Type_tt.CELL_CELL)
                for type_1 in Utils().get_device_types():
                    if True == self.get_netlist().is_in_cell(cell.get_name(), type_1):
                        subckt_type = self.get_subckt_type(type_1)
                        insert_name_cell_types.append([cell.get_name(), subckt_type])
                        delete_cell_keys.append(key_0)
                        break
        #
        for name, type in insert_name_cell_types:
            cell = Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)
            self.get_log().get_logger().info(
                f"cell({self.get_netlist().get_cell_key(name, type)}) is added"
            )
        #
        for delete_cell_key in delete_cell_keys:
            del self.get_netlist().get_cell_dic()[delete_cell_key]
            self.get_log().get_logger().info(f"cell({delete_cell_key}) is deleted")
        self.get_log().get_logger().info(
            f"# find subckt model end ... { datetime.datetime.now()}\n"
        )

    def run(self):
        self.get_log().get_logger().info(
            f"# read file({self.get_input().get_netlist_file_name()}) start ... {datetime.datetime.now()}\n"
        )
        #
        self.init_cell()
        self.get_netlist().print_info(self.get_log().get_logger())
        self.read_1st(self.get_input().get_netlist_file_name())
        self.find_subckt_model()
        self.get_netlist().print_info(self.get_log().get_logger())
        if True == self.get_input().get_debug():
            spc_1st_filename = f"{self.get_input().get_output_prefix()}.1st.spc"
            my_write = Write(self.get_input(), self.get_netlist(), 100, False, spc_1st_filename)
            my_write.run()
        #
        self.read_2nd(self.get_input().get_netlist_file_name())
        self.get_netlist().print_info(self.get_log().get_logger())
        if True == self.get_input().get_debug():
            spc_2nd_filename = f"{self.get_input().get_output_prefix()}.2nd.spc"
            my_write = Write(self.get_input(), self.get_netlist())
            my_write.set_file_name(spc_2nd_filename)
            my_write.run()
        #
        self.get_log().get_logger().info(
            f"# read file({self.get_input().get_netlist_file_name()}) end ... {datetime.datetime.now()}\n"
        )


def test_get_parameter_start_pos():
    my_parser = Parser()
    tokens = ["r1", "n1", "n2", "l", "=", "100u", "w", "=", "200u"]
    parameter_start_pos = my_parser.read_parameter_start_pos(tokens)
    print(f"{parameter_start_pos}")


def test_remove_comments():
    my_parser = Parser()
    line = "xname n1 n2 cell l='1*100' "
    line += 'w="200*300" * comments'
    lines = []
    lines.append(line)
    line = "* comment"
    lines.append(line)
    line = "r1 n1 n2 1000 $comment"
    lines.append(line)
    line = "$comment"
    lines.append(line)
    line = "xname n1 n2 cell $comment"
    lines.append(line)
    line = "xname n1 n2 cell $comment"
    lines.append(line)
    line = ".subckt a 1 2 l=100u w=200u $ aaa"
    lines.append(line)
    for line in lines:
        print(f"before : {line}")
        print(f"after  : {my_parser.remove_comments(line)}")
