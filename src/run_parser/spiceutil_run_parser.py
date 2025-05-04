import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import input
import log
import netlist
import version
import run
import run_write


class Parser(run.Run):
    def __init__(self, t_input=None, t_netlist=None):
        super().__init__(t_input, t_netlist)
        #
        self.m_cur_cell_name = netlist.k_DEFAULT_TOP_CELL_NAME()
        self.m_cur_cell = None
        # init default top cell
        self.m_default_top_cell = self.get_netlist().get_cell(
            netlist.k_DEFAULT_TOP_CELL_NAME(), netlist.Type.CELL_CELL
        )
        if None == self.m_default_top_cell:
            self.m_default_top_cell = netlist.Cell(
                netlist.k_DEFAULT_TOP_CELL_NAME(), netlist.Type.CELL_CELL
            )
            self.get_netlist().add_cell(self.m_default_top_cell)
            self.set_cur_cell(self.m_default_top_cell)

    def set_netlist(self, netlist):
        self.m_netlist = netlist

    def get_netlist(self):
        return self.m_netlist

    def set_cur_cell_name(self, cell_name):
        self.m_cur_cell_name = cell_name

    def get_cur_cell_name(self):
        return self.m_cur_cell_name

    def set_cur_cell(self, cell):
        self.m_cur_cell = cell

    def get_cur_cell(self):
        return self.m_cur_cell

    def get_default_top_cell(self):
        return self.m_default_top_cell

    def init_default_cell(self):
        self.get_input().get_log().get_logger().info(
            f"# init default cell start ... {datetime.datetime.now()}"
        )
        #
        for cell_type in netlist.k_DEFAULT_CELLS():
            cell_name = netlist.k_DEFAULT_CELL_DIC()[cell_type]
            cell_key = self.get_netlist().get_cell_key(cell_name, cell_type)
            cell = self.get_netlist().get_cell_by_cell_key(cell_key)
            if None == cell:
                cell = netlist.Cell(cell_name, cell_type)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
        #
        self.get_input().get_log().get_logger().info(
            f"# init default cell end ... {datetime.datetime.now()}\n"
        )

    def read_1st(self, file_name):
        self.get_input().get_log().get_logger().info(
            f"# read file({file_name}) 1st start ... {
            datetime.datetime.now()}"
        )
        nlines = 0
        total_line = ""
        with open(file_name, "rt") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                nlines = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    log.info(
                        f"{nlines} lines ... {
                             datetime.datetime.now()}"
                    )
                #
                if False == self.get_input().get_casesensitive():
                    line = line.lower()
                line = line.lstrip().rstrip()
                line = self.remove_comments(line, self.get_input().get_dollar_comment())
                if 0 == len(line):
                    continue
                #
                if "+" == line[0]:
                    total_line = total_line + line[1:]
                else:
                    self.read_total_line_1st(total_line, file_name)
                    total_line = line
        self.read_total_line_1st(total_line, file_name)
        self.get_input().get_log().get_logger().info(
            f"{nlines} lines ... {datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
            f"# read file({file_name}) 1st end ... {datetime.datetime.now()}\n"
        )

    def read_total_line_1st(self, total_line, file_name):
        t_total_line = total_line.replace("=", " = ")
        tokens = t_total_line.split()
        if 0 == len(tokens):
            return
        #
        if ".subckt" == tokens[0].lower():
            self.read_total_line_1st_subckt_line(tokens)
        elif ".ends" == tokens[0].lower():
            self.read_total_line_1st_ends_line()
        elif ".model" == tokens[0].lower():
            self.read_total_line_1st_model_line(tokens)
        elif (".inc" == tokens[0].lower()) or (".include" == tokens[0].lower()):
            self.read_total_line_1st_include_line(tokens, file_name)

    # .subckt name n1 n2 ... nN ...
    def read_total_line_1st_subckt_line(self, tokens):
        cell_name = tokens[1]
        cell_type = netlist.Type.CELL_CELL
        cell_key = self.get_netlist().get_cell_key(cell_name, cell_type)
        cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
            self.get_netlist().add_cell_key(cell_key)
            self.set_cur_cell(cell)
            self.set_cur_cell_name(cell_name)

    # .ends
    def read_total_line_1st_ends_line(self):
        self.set_cur_cell(self.get_default_top_cell())
        self.set_cur_cell_name(netlist.k_DEFAULT_TOP_CELL_NAME())

    # .model name modeltype ...
    def read_total_line_1st_model_line(self, tokens):
        model_name = tokens[1].split(".")[0]
        model_type = netlist.get_model_cell_type(tokens[2].lower())
        if netlist.Type.INIT == model_type:
            msg = f"# error: model name({model_name}) model type({model_type}) is unknown!"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        model_key = self.get_netlist().get_cell_key(model_name, model_type)
        model = self.get_netlist().get_cell_by_cell_key(model_key)
        if None == model:
            model = netlist.Cell(model_name, model_type)
            self.get_netlist().add_cell(model)
            self.get_netlist().add_cell_key(model_key)
            #
            self.get_cur_cell().add_cell(model)

    def read_total_line_1st_include_line(self, tokens, file_name):
        t_file_name = tokens[1].replace('"', "").replace("'", "")
        # 절대경로
        if "/" == t_file_name[0]:
            self.read_1st(t_file_name)
        # 상대경로
        else:
            absfile_name = os.path.abspath(file_name)
            absdirname = os.path.dirname(absfile_name)
            t_file_name = f"{absdirname}/{t_file_name}"
            self.read_1st(t_file_name)

    def read_2nd(self, file_name):
        self.get_input().get_log().get_logger().info(
            f"# read file({file_name}) 2nd start ... {
            datetime.datetime.now()}"
        )
        nlines = 0
        total_line = ""
        with open(file_name, "rt") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                nlines = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    self.get_input().get_log().get_logger().info(
                        f"{nlines} lines ... {
                        datetime.datetime.now()}"
                    )
                #
                if False == self.get_input().get_casesensitive():
                    line = line.lower()
                line = line.lstrip().rstrip()
                line = self.remove_comments(line, self.get_input().get_dollar_comment())
                if 0 == len(line):
                    continue
                #
                if "+" == line[0]:
                    total_line = total_line + line[1:]
                else:
                    self.read_total_line_2nd(total_line, file_name)
                    total_line = line
        self.read_total_line_2nd(total_line, file_name)
        self.get_input().get_log().get_logger().info(
            f"{nlines} lines ... {
            datetime.datetime.now()}"
        )
        self.get_input().get_log().get_logger().info(
            f"# read file({file_name}) 2nd end ... {datetime.datetime.now()}\n"
        )

    def read_total_line_2nd(self, total_line, file_name):
        t_total_line = total_line.replace("=", " = ")
        tokens = t_total_line.split()
        if 0 == len(tokens):
            return
        if ".subckt" == tokens[0].lower():
            self.read_total_line_2nd_subckt_line(tokens)
        elif ".ends" == tokens[0].lower():
            self.read_total_line_1st_ends_line()
        elif ".model" == tokens[0].lower():
            # TODO
            pass
        elif ".global" == tokens[0].lower():
            self.read_total_line_2nd_global_line(tokens)
        elif ".inc" == tokens[0] or ".include" == tokens[0]:
            self.read_total_line_2dn_include_line(tokens, file_name)
        elif (
            ("r" == tokens[0][0].lower())
            or ("c" == tokens[0][0].lower())
            or ("l" == tokens[0][0].lower())
        ):
            self.read_total_line_2nd_rlc_line(tokens)
        elif "k" == tokens[0][0].lower():
            self.read_total_line_2nd_k_line(tokens)
        elif ("v" == tokens[0][0].lower()) or ("i" == tokens[0][0].lower()):
            self.read_total_line_2nd_vs_cs_line(tokens)
        elif ("e" == tokens[0][0].lower()) or ("g" == tokens[0][0].lower()):
            self.read_total_line_2nd_vcvs_vccs_line(tokens)
        elif ("h" == tokens[0][0].lower()) or ("f" == tokens[0][0].lower()):
            self.read_total_line_2nd_ccvs_cccs_line(tokens)
        elif (
            ("d" == tokens[0][0].lower())
            or ("q" == tokens[0][0].lower())
            or ("m" == tokens[0][0].lower())
            or ("j" == tokens[0][0].lower())
        ):
            self.read_total_line_2nd_semiconductor_device_line(tokens)
        #            self.read_total_line_2nd_mosfet_line(tokens)
        #            self.read_total_line_2nd_bjt_line(tokens)
        #            self.read_total_line_2nd_jfet_line(tokens)
        elif "x" == tokens[0][0].lower():
            self.read_total_line_2nd_inst_line(tokens)

    def read_total_line_2nd_subckt_line(self, tokens):
        #
        cell_name = tokens[1]
        cell_type = netlist.Type.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            msg = f"cell({cell_name}) dont exist!"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        self.set_cur_cell(cell)
        #
        param_start_pos = self.get_param_start_pos(tokens)
        if -1 == param_start_pos:
            param_start_pos = len(tokens)
        for pos in range(2, param_start_pos):
            pin_name = tokens[pos]
            pin = cell.get_pin(pos - 2)
            if None == pin:
                pin = netlist.Node(pin_name, netlist.Type.NODE_PIN)
                cell.add_pin(pin)
            else:
                msg = f"# error : cell({cell_name}) pin({pin_name}) is duplicate!"
                self.get_input().get_log().get_logger().error(
                    f"{netlist.get_file_func_line_s(msg)}"
                )
                exit()
        #
        cell.make_pin_set()
        #
        self.read_params(cell, tokens, param_start_pos)

    # .global netnames...
    def read_total_line_2nd_global_line(self, tokens):
        for token in tokens[1:]:
            self.get_netlist().add_global_net_name(token)
        self.get_netlist().make_global_net_names_set()

    def read_total_line_2dn_include_line(self, tokens, file_name):
        t_file_name = tokens[1].replace('"', "").replace("'", "")
        # 절대경로
        if "/" == t_file_name[0]:
            self.read_1st(t_file_name)
        # 상대경로
        else:
            absfile_name = os.path.abspath(file_name)
            absdirname = os.path.dirname(absfile_name)
            t_file_name = f"{absdirname}/{t_file_name}"
            self.read_2nd(t_file_name)

    # rname n1 n2 value ...
    # lname n1 n2 value ...
    # cname n1 n2 value ...
    # rname n1 n2 model r = value ...
    # lname n1 n2 model l = value ...
    # cname n1 n2 model c = value ...

    def read_total_line_2nd_rlc_line(self, tokens):
        #
        inst_type = netlist.Type.INIT
        cell_type = netlist.Type.INIT
        if "r" == tokens[0][0]:
            inst_type = netlist.Type.INST_R
            cell_type = netlist.Type.CELL_R
        elif "l" == tokens[0][0]:
            inst_type = netlist.Type.INST_L
            cell_type = netlist.Type.CELL_L
        elif "c" == tokens[0][0]:
            inst_type = netlist.Type.INST_C
            cell_type = netlist.Type.CELL_C
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        param_start_pos = self.get_param_start_pos(tokens)
        # rname n1 n2 model r = value ...
        if 4 == param_start_pos and 4 < len(tokens):
            cell_name = tokens[param_start_pos - 1]
        # rname n1 n2 value
        cell_key = self.get_netlist().get_cell_key(cell_name, cell_type)
        cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        if None == cell:
            self.get_input().get_log().get_logger().warn(
                f"# warn: because model({cell_name}) isnot exist, so model({cell_name}) is generated!"
            )
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
            self.get_netlist().add_cell_key(cell_key)
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        # rname n1 n2 model r = value ...
        # lname n1 n2 model l = value ...
        # cname n1 n2 model c = value ...
        # print(f"# debug+++: {param_start_pos} {len(tokens)}")
        if 4 == param_start_pos and 4 < len(tokens):
            # print(f"# debug+++: ++1")
            self.read_params(inst, tokens, param_start_pos)
        # rname n1 n2 value ...
        # lname n1 n2 value ...
        # cname n1 n2 value ...
        else:
            # print(f"# debug+++: ++2")
            variable_name = cell_name
            inst.get_param().add_equation(variable_name, tokens[3], 0.0)
            self.read_params(inst, tokens, 4)
        #
        # print(f"# debug+++: {inst.get_info_str()}")

    # kname inductor1 inductor2 value

    def read_total_line_2nd_k_line(self, tokens):
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_K)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        cell_name = "k"
        cell_type = netlist.Type.CELL_K
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, 3):
            inductor_name = tokens[pos]
            inductor = self.get_cur_cell().get_inst(inductor_name)
            if None == inductor:
                inductor = netlist.Inst(inst_name, netlist.Type.INST_L)
                self.get_cur_cell().add_inst(inductor_name, inductor)
            inst.add_inst(inductor)
        #
        variable_name = cell_name
        inst.get_param().add_equation(variable_name, tokens[3], 0.0)

    # vname n1 n2 value
    # iname n1 n2 value

    def read_total_line_2nd_vs_cs_line(self, tokens):
        #
        inst_type = netlist.Type.INIT
        cell_type = netlist.Type.INIT
        if "v" == tokens[0][0]:
            inst_type = netlist.Type.INST_VS
            cell_type = netlist.Type.CELL_VS
        elif "i" == tokens[0][0]:
            inst_type = netlist.Type.INST_CS
            cell_type = netlist.Type.CELL_CS
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        variable_name = "dc"
        inst.get_param().add_equation(variable_name, tokens[3], 0.0)

    # VCVS
    # Ename N1 N2 NC1 NC2 value
    # VCCS
    # Gname N1 N2 NC1 NC2 value

    def read_total_line_2nd_vcvs_vccs_line(self, tokens):
        #
        inst_type = netlist.Type.INIT
        cell_type = netlist.Type.INIT
        if "e" == tokens[0][0]:
            inst_type = netlist.Type.INST_VCVS
            cell_type = netlist.Type.CELL_VCVS
        elif "g" == tokens[0][0]:
            inst_type = netlist.Type.INST_VCCS
            cell_type = netlist.Type.CELL_VCCS
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        cell_key = self.get_netlist().get_cell_key(cell_name, cell_type)
        cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
            self.get_netlist().add_cell_key(cell_key)
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, 5):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        variable_name = cell_name
        inst.get_param().add_equation(variable_name, tokens[5], 0.0)
        #
        # print(f"# debug+++: {inst.get_info_str()}")

    # CCVS
    # Hname N1 N2 VControl value
    # CCCS
    # Fname N1 N2 VControl value

    def read_total_line_2nd_ccvs_cccs_line(self, tokens):
        #
        inst_type = netlist.Type.INIT
        cell_type = netlist.Type.INIT
        if "h" == tokens[0][0]:
            inst_type = netlist.Type.INST_CCVS
            cell_type = netlist.Type.CELL_CCVS
        elif "f" == tokens[0][0]:
            inst_type = netlist.Type.INST_CCCS
            cell_type = netlist.Type.CELL_CCCS
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            cell = netlist.Cell(cell_name, cell_type)
            self.get_netlist().add_cell(cell)
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, 3):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        vcontrol_name = tokens[3]
        vcontrol = self.get_cur_cell().get_inst(vcontrol_name)
        if None == vcontrol:
            vcontrol = netlist.Inst(vcontrol_name, netlist.Type.INST_VS)
            print(f"{vcontrol}")
            self.get_cur_cell().add_inst(vcontrol)
        inst.add_inst(vcontrol)
        #
        variable_name = cell_name
        inst.get_param().add_equation(variable_name, tokens[4], 0.0)
        #
        # print(f"# debug+++: {inst.get_info_str()}")

    # dname n1 n2 model ...
    # jname n1 n2 n3 model ...
    # qname n1 n2 n3 model ...
    # mname n1 n2 n3 n4 model l = 100u w = 200u ...

    def read_total_line_2nd_semiconductor_device_line(self, tokens):
        #
        inst_type = netlist.Type.INIT
        cell_type = netlist.Type.INIT
        if "d" == tokens[0][0].lower():
            inst_type = netlist.Type.INST_DIODE
            cell_type = netlist.Type.CELL_DIODE
        elif "j" == tokens[0][0].lower():
            inst_type = netlist.Type.INST_JFET
            cell_type = netlist.Type.CELL_JFET
        elif "q" == tokens[0][0].lower():
            inst_type = netlist.Type.INST_BJT
            cell_type = netlist.Type.CELL_BJT
        elif "m" == tokens[0][0].lower():
            inst_type = netlist.Type.INST_MOSFET
            cell_type = netlist.Type.CELL_MOSFET
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        param_start_pos = self.get_param_start_pos(tokens)
        cell_pos = param_start_pos - 1
        cell_name = tokens[cell_pos]
        cell = None
        #
        if netlist.Type.CELL_DIODE == cell_type:
            cell_key = self.get_netlist().get_cell_key(cell_name, netlist.Type.CELL_DIODE)
            cell = self.get_netlist().get_cell_by_cell_key(cell_key)
            if None == cell:
                cell_key = self.get_netlist().get_cell_key(cell_name, netlist.Type.CELL_DIODE)
                cell = netlist.Cell(cell_name, netlist.Type.CELL_DIODE)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
        elif netlist.Type.CELL_BJT == cell_type:
            for cell_type_t in [
                netlist.Type.CELL_BJT_NPN,
                netlist.Type.CELL_BJT_PNP,
                netlist.Type.CELL_BJT,
            ]:
                cell_key = self.get_netlist().get_cell_key(cell_name, cell_type_t)
                cell = self.get_netlist().get_cell_by_cell_key(cell_key)
                if None != cell:
                    break
            if None == cell:
                cell_key = self.get_netlist().get_cell_key(cell_name, netlist.Type.CELL_BJT)
                cell = netlist.Cell(cell_name, netlist.Type.CELL_BJT)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
        elif netlist.Type.CELL_JFET == cell_type:
            for cell_type_t in [
                netlist.Type.CELL_JFET_NJF,
                netlist.Type.CELL_JFET_PJF,
                netlist.Type.CELL_JFET,
            ]:
                cell_key = self.get_netlist().get_cell_key(cell_name, cell_type_t)
                cell = self.get_netlist().get_cell_by_cell_key(cell_key)
                if None != cell:
                    break
            if None == cell:
                cell_key = self.get_netlist().get_cell_key(cell_name, netlist.Type.CELL_JFET)
                cell = netlist.Cell(cell_name, netlist.Type.CELL_JFET)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
        elif netlist.Type.CELL_MOSFET == cell_type:
            for cell_type_t in [
                netlist.Type.CELL_MOSFET_NMOS,
                netlist.Type.CELL_MOSFET_PMOS,
                netlist.Type.CELL_MOSFET,
            ]:
                cell_key = self.get_netlist().get_cell_key(cell_name, cell_type_t)
                cell = self.get_netlist().get_cell_by_cell_key(cell_key)
                if None != cell:
                    break
            if None == cell:
                cell_key = self.get_netlist().get_cell_key(cell_name, netlist.Type.CELL_MOSFET)
                cell = netlist.Cell(cell_name, netlist.Type.CELL_MOSFET)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
        else:
            msg = (
                f"# error: model({cell_name}-{cell_type}) isnot exist!({self.get_cur_cell_name()})"
            )
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()

        #
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, cell_pos):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        self.read_params(inst, tokens, param_start_pos)

    # xname n1 n2 ... cell ...

    def read_total_line_2nd_inst_line(self, tokens):
        inst_name = tokens[0]
        cur_cell = self.get_cur_cell()
        inst = cur_cell.get_inst(inst_name)
        # inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_INST)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error : inst({inst_name}) is duplicate in cell({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        parameter_start_pos = self.get_param_start_pos(tokens)
        cell_name = tokens[parameter_start_pos - 1].lower()
        cell_type = netlist.Type.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in netlist.get_subckt_types_set():
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
            if None == cell:
                self.get_input().get_log().get_logger().error(
                    f"{netlist.get_file_func_line_s(msg)}"
                )
                exit()
        #
        parameter_start_pos = self.get_param_start_pos(tokens)
        cell_name = tokens[parameter_start_pos - 1].lower()
        cell_type = netlist.Type.CELL_CELL
        cell = self.get_netlist().get_cell(cell_name, cell_type)
        if None == cell:
            for cell_type in netlist.get_subckt_types_set():
                cell = self.get_netlist().get_cell(cell_name, cell_type)
                if None != cell:
                    break
            if None == cell:
                msg = f"# error : inst({inst_name}) cell({cell_name}) isnot exist!"
                self.get_input().get_log().get_logger().error(
                    f"{netlist.get_file_func_line_s(msg)}"
                )
                exit()
        #
        inst.set_cell(cell)
        #
        for pos in range(1, parameter_start_pos - 1):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
        #
        inst.set_cell(cell)
        cell.increase_inst_count()
        #
        for pos in range(1, parameter_start_pos - 1):
            node_name = tokens[pos]
            node = self.get_cur_cell().get_node(node_name)
            if None == node:
                node = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.get_cur_cell().add_node(node)
            inst.add_node(node)
            node.add_inst(inst)
        #
        self.read_params(inst, tokens, parameter_start_pos)

    def get_param_start_pos(self, tokens):
        params_start_pos = len(tokens)
        for pos in range(1, len(tokens)):
            if "=" == tokens[pos]:
                params_start_pos = pos - 1
                break
        return params_start_pos

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

    def read_params(self, inst_cell, tokens, params_start_pos):
        variable_name_pos = params_start_pos
        equation_start_pos = len(tokens)
        equation_end_pos = len(tokens)
        for pos in range(len(tokens) - 1, params_start_pos, -1):
            if "=" == tokens[pos]:
                variable_name_pos = pos - 1
                equation_start_pos = pos + 1
                variable_name = tokens[variable_name_pos]
                equation_s = " ".join(tokens[equation_start_pos:equation_end_pos])
                equation_s = (
                    equation_s.replace(" ", "").replace("\t", "").replace("'", "").replace('"', "")
                )
                inst_cell.get_param().add_equation(variable_name, equation_s, 0.0)
                equation_end_pos = variable_name_pos

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

    def run(self):
        self.get_input().get_log().get_logger().info(
            f"# read file({self.get_input().get_spice_file_name()}) start ... {datetime.datetime.now()}\n"
        )
        #
        self.init_default_cell()
        self.get_input().get_log().get_logger().info(self.get_netlist().get_cell_summary_str())
        #
        self.read_1st(self.get_input().get_spice_file_name())
        self.get_input().get_log().get_logger().info(self.get_netlist().get_cell_summary_str())
        #
        # self.find_subckt_model()
        # self.get_input().get_log().get_logger().info(f"P{self.get_netlist().get_summary_str()}")
        if True == self.get_input().get_is_write_1st_spc():
            spc_1st_file_name = f"{self.get_input().get_output_prefix()}.1st.spc"
            self.get_input().get_log().get_logger().info(
                f"# write 1st spc file({spc_1st_file_name}) ... {datetime.datetime.now()}\n"
            )
            my_write = run_write.Write(self.get_input(), self.get_netlist())
            my_write.set_file_name(spc_1st_file_name)
            my_write.run()
        #
        self.read_2nd(self.get_input().get_spice_file_name())
        self.get_input().get_log().get_logger().info(self.get_netlist().get_cell_summary_str())
        # self.get_netlist().print_info(self.get_input().get_log().get_logger())
        if True == self.get_input().get_is_write_2nd_spc():
            spc_2nd_file_name = f"{self.get_input().get_output_prefix()}.2nd.spc"
            self.get_input().get_log().get_logger().info(
                f"# write 2nd spc file({spc_2nd_file_name}) ... {datetime.datetime.now()}\n"
            )
            my_write = run_write.Write(self.get_input(), self.get_netlist())
            my_write.set_file_name(spc_2nd_file_name)
            my_write.run()
        #
        self.get_input().get_log().get_logger().info(
            f"# read file({self.get_input().get_spice_file_name()}) end ... {datetime.datetime.now()}\n"
        )


def test_get_parameter_start_pos():
    my_parser = Parser()
    tokens = ["r1", "n1", "n2", "l", "=", "100u", "w", "=", "200u"]
    parameter_start_pos = my_parser.get_param_start_pos(tokens)
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
