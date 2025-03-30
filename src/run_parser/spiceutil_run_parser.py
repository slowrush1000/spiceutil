import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import log
import netlist
import version
import run


class Parser(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)
        #
        self.m_cur_cellname = netlist.get_k_default_top_cellname()
        self.m_cur_cell = None
        #
        # print(f"#debug- {self.get_netlist()}")
        # print(f"#debug- {netlist.get_k_default_top_cellname()}")
        self.m_default_top_cell = self.get_netlist().get_cell(
            netlist.get_k_default_top_cellname(), netlist.Type.CELL_CELL
        )
        if None == self.m_default_top_cell:
            self.m_default_top_cell = netlist.Cell(
                netlist.get_k_default_top_cellname(), netlist.Type.CELL_CELL
            )
            self.m_netlist.add_cell(
                netlist.get_k_default_top_cellname(),
                self.m_default_top_cell,
                netlist.Type.CELL_CELL,
            )

    def set_netlist(self, netlist):
        self.m_netlist = netlist

    def get_netlist(self):
        return self.m_netlist

    def set_cur_cellname(self, cellname):
        self.m_cur_cellname = cellname

    def get_cur_cellname(self):
        return self.m_cur_cellname

    def set_cur_cell(self, cell):
        self.m_cur_cell = cell

    def get_cur_cell(self):
        return self.m_cur_cell

    def get_default_top_cell(self):
        return self.m_default_top_cell

    def init_cell(self):
        self.get_input().get_log().get_logger().info(f"# init cell start")
        for type in netlist.get_k_default_cellname_dic():
            name = netlist.get_k_default_cellname_dic()[type]
            cell = netlist.Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)
        self.get_input().get_log().get_logger().info(f"# init cell end")

    def read_1st(self, filename):
        self.get_input().get_log().get_logger().info(
            f"# read file({filename}) 1st start ... {
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
                if 0 == (nlines % netlist.get_k_line_step()):
                    log.info(
                        f"    {nlines} lines ... {
                             datetime.datetime.now()}"
                    )
                #
                if False == self.get_input().get_casesensitive():
                    line = line.lower()
                line = line.lstrip().rstrip()
                line = self.remove_comments(
                    line, self.get_input().get_dollar_comment()
                )
                if 0 == len(line):
                    continue
                #
                if "+" == line[0]:
                    total_line = total_line + line[1:]
                else:
                    self.read_total_line_1st(total_line, filename)
                    total_line = line
        self.read_total_line_1st(total_line, filename)
        self.get_input().get_log().get_logger().info(
            f"    {nlines} lines ... {
            datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
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
        elif (".inc" == tokens[0].lower()) or (
            ".include" == tokens[0].lower()
        ):
            self.read_total_line_1st_include_line(tokens, filename)

    def read_total_line_1st_subckt_line(self, tokens):
        name = tokens[1]
        type = netlist.Type.CELL_CELL
        if False == self.get_netlist().is_exist_cell(name, type):
            cell = netlist.Cell(name, type)
            self.set_cur_cellname(name)
            self.get_netlist().add_cell(name, cell, type)

    def read_total_line_1st_ends_line(self):
        self.set_cur_cellname(netlist.get_k_default_top_cellname())
        self.set_cur_cell(self.get_default_top_cell())

    def read_total_line_1st_model_line(self, tokens):
        name = tokens[1].split(".")[0]
        type_name = tokens[2]
        type = netlist.Type.INIT
        if "d" == type_name:
            type = netlist.Type.CELL_DIODE
        elif "npn" == type_name:
            type = netlist.Type.CELL_NPN
        elif "pnp" == type_name:
            type = netlist.Type.CELL_PNP
        elif "nmos" == type_name:
            type = netlist.Type.CELL_NMOS
        elif "pmos" == type_name:
            type = netlist.Type.CELL_PMOS
        elif "njf" == type_name:
            type = netlist.Type.CELL_NJF
        elif "pjf" == type_name:
            type = netlist.Type.CELL_PJF
        #
        if False == self.get_netlist().is_exist_cell(name, type):
            cell = netlist.Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)

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
        self.get_input().get_log().get_logger().info(
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
                if 0 == (nlines % netlist.get_k_line_step()):
                    self.get_log().get_logger().info(
                        f"    {nlines} lines ... {
                        datetime.datetime.now()}"
                    )
                #
                if False == self.get_input().get_casesensitive():
                    line = line.lower()
                line = line.lstrip().rstrip()
                line = self.remove_comments(
                    line, self.get_input().get_dollar_comment()
                )
                if 0 == len(line):
                    continue
                #
                if "+" == line[0]:
                    total_line = total_line + line[1:]
                else:
                    self.read_total_line_2nd(total_line, filename)
                    total_line = line
        self.read_total_line_2nd(total_line, filename)
        self.get_input().get_log().get_logger().info(
            f"    {nlines} lines ... {
            datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
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
        elif netlist.get_k_default_cellname_r() == tokens[0][0]:
            self.read_total_line_2nd_r_line(tokens)
        elif netlist.get_k_default_cellname_c() == tokens[0][0]:
            self.read_total_line_2nd_c_line(tokens)
        elif netlist.get_k_default_cellname_l() == tokens[0][0]:
            self.read_total_line_2nd_l_line(tokens)
        elif netlist.get_k_default_cellname_k() == tokens[0][0]:
            self.read_total_line_2nd_k_line(tokens)
        elif netlist.get_k_default_cellname_vs() == tokens[0][0]:
            self.read_total_line_2nd_vs_line(tokens)
        elif netlist.get_k_default_cellname_cs() == tokens[0][0]:
            self.read_total_line_2nd_cs_line(tokens)
        elif netlist.get_k_default_cellname_vcvs() == tokens[0][0]:
            self.read_total_line_2nd_vcvs_line(tokens)
        elif netlist.get_k_default_cellname_ccvs() == tokens[0][0]:
            self.read_total_line_2nd_ccvs_line(tokens)
        elif netlist.get_k_default_cellname_vccs() == tokens[0][0]:
            self.read_total_line_2nd_vccs_line(tokens)
        elif netlist.get_k_default_cellname_cccs() == tokens[0][0]:
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
        cell_type = netlist.Type.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in netlist.get_subckt_types_set():
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
        if None == cell:
            msg = f"cell({cell_name}) dont exist!"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        self.set_cur_cell(cell)
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        if -1 == parameter_start_pos:
            parameter_start_pos = len(tokens)
        for pos in range(2, parameter_start_pos):
            # self.get_log().get_logger().debug(f'{cell_name} - {tokens[pos]}')
            pin_name = tokens[pos]
            if False == cell.is_exist_node(pin_name):
                # self.get_log().get_logger().debug(f'{cell_name} - {pin_name}')
                pin = netlist.Node(pin_name, netlist.Type.NODE_PIN)
                cell.add_pin(pin_name, pin)
            else:
                msg = f"# error : cell({cell_name}) pin({pin_name}) is duplicate!"
                self.get_log().get_logger().error(
                    f"{netlist.get_error_str(msg)}"
                )
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
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_R)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = netlist.get_k_default_cellname_r()
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        # self.get_log().get_logger().debug(f'debug- {cell_name}')
        # rname n1 n2 value
        cell_type = netlist.Type.CELL_R
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        # rname n1 n2 value
        else:
            parameter_name = netlist.get_k_default_cellname_r()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # cname n1 n2 value

    def read_total_line_2nd_c_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_C)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = netlist.get_k_default_cellname_c()
        # cname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        cell_type = netlist.Type.CELL_C
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        else:
            parameter_name = netlist.get_k_default_cellname_c()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # lname n1 n2 value

    def read_total_line_2nd_l_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_L)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = netlist.get_k_default_cellname_l()
        # lname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name = tokens[parameter_start_pos - 1]
        cell_type = netlist.Type.CELL_L
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.read_parameter_inst(inst, tokens, parameter_start_pos)
        else:
            parameter_name = netlist.get_k_default_cellname_l()
            parameter_equation = tokens[3]
            inst.add_parameter(parameter_name, parameter_equation)

    # kname inductor1 inductor2 value

    def read_total_line_2nd_k_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_K)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_k()
        cell_type = netlist.Type.CELL_K
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            inductor_name = tokens[pos]
            inductor = self.get_cur_cell().get_inst(inductor_name)
            if None == inductor:
                inductor = netlist.Inst(inst_name, netlist.Type.INST_L)
                self.get_cur_cell().add_inst(inductor_name, inductor)
            inst.add_inst(inductor)
        #
        parameter_name = netlist.get_k_default_cellname_k()
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # vname n1 n2 value

    def read_total_line_2nd_vs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_VS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_vs()
        cell_type = netlist.Type.CELL_VS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = "dc"
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # iname n1 n2 value

    def read_total_line_2nd_cs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_CS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_k()
        cell_type = netlist.Type.CELL_K
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = "dc"
        parameter_equation = tokens[3]
        inst.add_parameter(parameter_name, parameter_equation)

    # ename n1 n2 nc1 nc2 value

    def read_total_line_2nd_vcvs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_VCVS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_vcvs()
        cell_type = netlist.Type.CELL_VCVS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = netlist.get_k_default_cellname_vcvs()
        parameter_equation = tokens[5]
        inst.add_parameter(parameter_name, parameter_equation)

    # gname n1 n2 nc1 nc2 value

    def read_total_line_2nd_ccvs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_CCVS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_ccvs()
        cell_type = netlist.Type.CELL_CCVS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        parameter_name = netlist.get_k_default_cellname_ccvs()
        parameter_equation = tokens[5]
        inst.add_parameter(parameter_name, parameter_equation)

    # hname n1 n2 vcontrol value

    def read_total_line_2nd_vccs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_VCCS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_vccs()
        cell_type = netlist.Type.CELL_VCCS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        vcontrol_name = tokens[3]
        vcontrol = self.get_cur_cell().get_inst(vcontrol_name)
        if None == vcontrol:
            vcontrol = netlist.Inst(vcontrol_name, netlist.Type.INST_VS)
            self.get_cur_cell().add_inst(vcontrol_name, vcontrol)
        inst.add_inst(vcontrol)
        #
        parameter_name = netlist.get_k_default_cellname_vccs()
        parameter_equation = tokens[4]
        inst.add_parameter(parameter_name, parameter_equation)

    # fname n1 n2 vcontrol value

    def read_total_line_2nd_cccs_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_CCCS)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        cell_name = netlist.get_k_default_cellname_cccs()
        cell_type = netlist.Type.CELL_CCCS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
        #
        vcontrol_name = tokens[3]
        vcontrol = self.get_cur_cell().get_inst(vcontrol_name)
        if None == vcontrol:
            vcontrol = netlist.Inst(vcontrol_name, netlist.Type.INST_VS)
            self.get_cur_cell().add_inst(vcontrol_name, vcontrol)
        inst.add_inst(vcontrol)
        #
        parameter_name = netlist.get_k_default_cellname_cccs()
        parameter_equation = tokens[4]
        inst.add_parameter(parameter_name, parameter_equation)

    # mname n1 n2 n3 n4 cellname l = 100u w = 200u

    def read_total_line_2nd_mosfet_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_MOSFET)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 6
        cell_name = tokens[5].lower()
        cell_type = netlist.Type.CELL_NMOS
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = netlist.Type.CELL_PMOS
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = netlist.Type.CELL_MOSFET
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = netlist.Type.CELL_MOSFET
                    cell = netlist.Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # qname n1 n2 n3 model ...

    def read_total_line_2nd_bjt_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_BJT)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 5
        cell_name = tokens[4].lower()
        cell_type = netlist.Type.CELL_NPN
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = netlist.Type.CELL_PNP
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = netlist.Type.CELL_BJT
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = netlist.Type.CELL_BJT
                    cell = netlist.Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 4):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # jname n1 n2 n3 model ...

    def read_total_line_2nd_jfet_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_JFET)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 5
        cell_name = tokens[4].lower()
        cell_type = netlist.Type.CELL_JFET
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell_type = netlist.Type.CELL_PJF
            cell = self.get_netlist().get_cell(cell_name, cell_type)
            if None == cell:
                cell_type = netlist.Type.CELL_NJF
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None == cell:
                    cell_type = netlist.Type.CELL_JFET
                    cell = netlist.Cell(cell_name, cell_type)
                    self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 4):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # dname n1 n2 model ...

    def read_total_line_2nd_diode_line(self, tokens):
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_DIODE)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = 4
        cell_name = tokens[3].lower()
        cell_type = netlist.Type.CELL_DIODE
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell_name, cell, cell_type)
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
        #
        self.read_parameter_inst(inst, tokens, parameter_start_pos)

    # xname n1 n2 ... cell ...

    def read_total_line_2nd_inst_line(self, tokens):
        inst_name = tokens[0]
        cur_cell = self.get_cur_cell()
        inst = cur_cell.get_inst(inst_name)
        # inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_INST)
            self.get_cur_cell().add_inst(inst_name, inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cellname()})"
            self.get_log().get_logger().error(f"{netlist.get_error_str(msg)}")
            exit()
        #
        parameter_start_pos = self.read_parameter_start_pos(tokens)
        cell_name = tokens[parameter_start_pos - 1].lower()
        cell_type = netlist.Type.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in netlist.get_subckt_types_set():
                # for cell_type in netlist.k_SUBCKT_TYPES:
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
            if None == cell:
                msg = f"# error : inst({inst_name}) cell({cell_name}) isnot exist!"
                msg += netlist.get_trace_info_str()
                self.get_log().get_logger().error(msg)
            # cell_type = netlist.Type.CELL_CELL
            # cell = self.get_netlist().get_cell(cell_name, cell_type)
            # cell = netlist.Cell(cell_name, cell_type)
            # self.get_netlist().add_cell(cell_name, cell, cell_type)
        #
        inst.set_cell(cell)
        cell.increase_inst_size()
        #
        for pos in range(1, parameter_start_pos - 1):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node_name, node)
            inst.add_node(node)
            node.add_inst(inst_name, inst)
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
        equation_start_pos = len(tokens)
        equation_end_pos = len(tokens)
        for pos in range(len(tokens) - 1, parameter_start_pos, -1):
            if "=" == tokens[pos]:
                name_pos = pos - 1
                equation_start_pos = pos + 1
                # self.get_log().get_logger().debug(f'debug : pos : {pos} name_pos : {name_pos} equation_start_pos : {equation_start_pos} equation_end_pos : {equation_end_pos}')
                name = tokens[name_pos]
                equation = " ".join(
                    tokens[equation_start_pos:equation_end_pos]
                )
                equation = (
                    equation.replace(" ", "")
                    .replace("\t", "")
                    .replace("'", "")
                    .replace('"', "")
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
                equation = " ".join(
                    tokens[equation_start_pos:equation_end_pos]
                )
                equation = (
                    equation.replace(" ", "")
                    .replace("\t", "")
                    .replace("'", "")
                    .replace('"', "")
                )
                inst.add_parameter(name, equation)
                equation_end_pos = name_pos

    def get_subckt_type(self, type):
        match type:
            case netlist.Type.CELL_DIODE:
                return netlist.Type.CELL_CELL_DIODE
            case netlist.Type.CELL_NMOS:
                return netlist.Type.CELL_CELL_NMOS
            case netlist.Type.CELL_PMOS:
                return netlist.Type.CELL_CELL_PMOS
            case netlist.Type.CELL_NPN:
                return netlist.Type.CELL_CELL_NPN
            case netlist.Type.CELL_PNP:
                return netlist.Type.CELL_CELL_PNP
            case netlist.Type.CELL_NJF:
                return netlist.Type.CELL_CELL_NJF
            case netlist.Type.CELL_PJF:
                return netlist.Type.CELL_CELL_PJF
            case _:
                return netlist.Type.INIT

    def find_subckt_model(self):
        self.get_input().get_log().get_logger().info(
            f"# find subckt model start ... {datetime.datetime.now()}"
        )
        #
        insert_name_cell_types = []
        delete_cell_keys = []
        for key in self.get_netlist().get_cell_dic():
            cell = self.get_netlist().get_cell_by_key(key)
            if netlist.Type.CELL_CELL == cell.get_type():
                key_0 = self.get_netlist().get_cell_key(
                    cell.get_name(), netlist.Type.CELL_CELL
                )
                for type_1 in netlist.get_device_types():
                    if True == self.get_netlist().is_exist_cell(
                        cell.get_name(), type_1
                    ):
                        subckt_type = self.get_subckt_type(type_1)
                        insert_name_cell_types.append(
                            [cell.get_name(), subckt_type]
                        )
                        delete_cell_keys.append(key_0)
                        break
        #
        for name, type in insert_name_cell_types:
            cell = netlist.Cell(name, type)
            self.get_netlist().add_cell(name, cell, type)
            self.get_input().get_log().get_logger().info(
                f"cell({self.get_netlist().get_cell_key(name, type)}) is added"
            )
        #
        for delete_cell_key in delete_cell_keys:
            del self.get_netlist().get_cell_dic()[delete_cell_key]
            self.get_input().get_log().get_logger().info(
                f"cell({delete_cell_key}) is deleted"
            )
        self.get_input().get_log().get_logger().info(
            f"# find subckt model end ... { datetime.datetime.now()}\n"
        )

    def run(self):
        self.get_input().get_log().get_logger().info(
            f"# read file({self.get_input().get_spice_filename()}) start ... {datetime.datetime.now()}\n"
        )
        #
        self.init_cell()
        self.get_netlist().print_info(self.get_input().get_log().get_logger())
        self.read_1st(self.get_input().get_spice_filename())
        # self.get_netlist().print_info(self.get_input().get_log().get_logger())
        self.find_subckt_model()
        # self.get_netlist().print_info(self.get_input().get_log().get_logger())
        if True == self.get_input().get_is_write_1st_spc():
            spc_1st_filename = (
                f"{self.get_input().get_output_prefix()}.1st.spc"
            )
            self.get_netlist().write_netlist(
                self.get_input().get_log().get_logger(),
                spc_1st_filename,
                self.get_input().get_text_width(),
                self.get_input().get_version().get_info_str(),
            )
        #
        self.read_2nd(self.get_input().get_spice_filename())
        self.get_netlist().print_info(self.get_input().get_log().get_logger())
        self.get_netlist().print_inst_info(
            self.get_input().get_log().get_logger()
        )
        if True == self.get_input().get_is_write_2nd_spc():
            spc_2nd_filename = (
                f"{self.get_input().get_output_prefix()}.2nd.spc"
            )
            self.get_netlist().write_netlist(
                self.get_input().get_log().get_logger(),
                spc_2nd_filename,
                self.get_input().get_text_width(),
                self.get_input().get_version().get_info_str(),
            )
        #
        self.get_input().get_log().get_logger().info(
            f"# read file({self.get_input().get_spice_filename()}) end ... {datetime.datetime.now()}\n"
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


#
if __name__ == "__main__":
    # TestGetParameterStartPos()
    test_remove_comments()
