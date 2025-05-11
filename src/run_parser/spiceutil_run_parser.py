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
        cell_key = netlist.get_cell_key(netlist.k_DEFAULT_TOP_CELL_NAME(), netlist.Type.CELL_CELL)
        self.m_default_top_cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        if None == self.m_default_top_cell:
            self.m_default_top_cell = netlist.Cell(
                netlist.k_DEFAULT_TOP_CELL_NAME(), netlist.Type.CELL_CELL
            )
            self.get_netlist().add_cell(self.m_default_top_cell)
            self.get_netlist().add_cell_key(cell_key)
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
            cell_key = netlist.get_cell_key(cell_name, cell_type)
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
        self.add_cell_model_1st(cell_name, cell_type)

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
        self.add_cell_model_1st(model_name, model_type)

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
        elif "x" == tokens[0][0].lower():
            self.read_total_line_2nd_inst_line(tokens)

    def read_total_line_2nd_subckt_line(self, tokens):
        #
        cell_name = tokens[1]
        cell_type = netlist.Type.CELL_CELL
        cell_key = netlist.get_cell_key(cell_name, cell_type)
        cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        if None == cell:
            cell = self.get_cur_cell().get_cell_by_cell_key(cell_key)
            if None == cell:
                msg = f"cell({cell_name}) dont exist!"
                self.get_input().get_log().get_logger().error(
                    f"{netlist.get_file_func_line_s(msg)}"
                )
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
                msg = f"# error: cell({cell_name}) pin({pin_name}) is duplicate!"
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
        #
        inst_type, cell_type = netlist.get_inst_type_cell_type(tokens[0][0].lower())
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        param_start_pos = self.get_param_start_pos(tokens)
        # rname n1 n2 model r = value ...
        if 4 == param_start_pos and 4 < len(tokens):
            cell_name = tokens[param_start_pos - 1]
        # rname n1 n2 value
        k_cells = [netlist.Type.CELL_R, netlist.Type.CELL_C, netlist.Type.CELL_L]
        cell = self.get_cell_from_local_global(
            inst_name, cell_name, k_cells, self.get_input().get_malias()
        )
        # cell_key = netlist.get_cell_key(cell_name, cell_type)
        #        cell = self.get_netlist().get_cell_by_cell_key(cell_key)
        #        if None == cell:
        #            if True == self.get_input().get_malias():
        #                self.get_input().get_log().get_logger().warn(
        #                    f"# warn: because model({cell_name}) isnot exist, so model({cell_name}) is generated!"
        #                )
        #                cell = netlist.Cell(cell_name, cell_type)
        #                self.get_netlist().add_cell(cell)
        #                self.get_netlist().add_cell_key(cell_key)
        #            else:
        #                msg = (
        #                    f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
        #                )
        #                self.get_input().get_log().get_logger().error(
        #                    f"{netlist.get_file_func_line_s(msg)}"
        #                )
        #                exit()
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
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
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
        inst_type, cell_type = netlist.get_inst_type_cell_type(tokens[0][0].lower())
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
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
        inst_type, cell_type = netlist.get_inst_type_cell_type(tokens[0][0].lower())
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        cell_key = netlist.get_cell_key(cell_name, cell_type)
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
        inst_type, cell_type = netlist.get_inst_type_cell_type(tokens[0][0].lower())
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
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
        inst_type, cell_type = netlist.get_inst_type_cell_type(tokens[0][0].lower())
        cell_name = tokens[0][0].lower()
        #
        inst_name = tokens[0]
        inst = self.get_cur_cell().get_inst(inst_name)
        if None == inst:
            inst = netlist.Inst(inst_name, inst_type)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in subckt({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        param_start_pos = self.get_param_start_pos(tokens)
        cell_pos = param_start_pos - 1
        cell_name = tokens[cell_pos]
        cell = self.get_semiconductor_cell(inst_name, cell_name, cell_type)
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
        if None == inst:
            inst = netlist.Inst(inst_name, netlist.Type.INST_INST)
            self.get_cur_cell().add_inst(inst)
        else:
            msg = f"# error: inst({inst_name}) is duplicate in cell({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()
        #
        params_start_pos = self.get_param_start_pos(tokens)
        cell_pos = params_start_pos - 1
        #
        cell_name = tokens[cell_pos]
        cell = self.get_cell_from_local_global(inst_name, cell_name, [netlist.Type.CELL_CELL])
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
        self.read_params(inst, tokens, params_start_pos)

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

    def add_cell_model_1st(self, cell_name, cell_type):
        # global
        cell_key = netlist.get_cell_key(cell_name, cell_type)
        if netlist.k_DEFAULT_TOP_CELL_NAME() == self.get_cur_cell_name():
            cell = self.get_netlist().get_cell_by_cell_key(cell_key)
            if None == cell:
                cell = netlist.Cell(cell_name, cell_type)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
                if netlist.Type.CELL_CELL == cell_type:
                    self.set_cur_cell(cell)
                    self.set_cur_cell_name(cell_name)
        # local
        else:
            cell = self.get_cur_cell().get_cell_by_cell_key(cell_key)
            if None == cell:
                cell = netlist.Cell(cell_name, cell_type)
                self.get_cur_cell().add_cell(cell)
                self.get_cur_cell().add_cell_key(cell_key)
                if netlist.Type.CELL_CELL == cell_type:
                    self.set_cur_cell(cell)
                    self.set_cur_cell_name(cell_name)

    def get_cell_from_local_global(self, inst_name, cell_name, cell_types, malias=False):
        for cell_type in cell_types:
            cell_key = netlist.get_cell_key(cell_name, cell_type)
            cell = self.get_cur_cell().get_cell_by_cell_key(cell_key)
            if None != cell:
                return cell
            else:
                cell = self.get_netlist().get_cell_by_cell_key(cell_key)
                if None != cell:
                    return cell
        #
        if None == cell:
            if True == malias:
                msg = f"# warn: because model({cell_name}) isnot exist, so model({cell_name}) is generated!"
                self.get_input().get_log().get_logger().warn(f"{msg}")
                cell = netlist.Cell(cell_name, cell_type)
                self.get_netlist().add_cell(cell)
                self.get_netlist().add_cell_key(cell_key)
                return cell
            else:
                msg = f"# error: model({cell_name}-{cell_type}) of inst({inst_name}) isnot exist!({self.get_cur_cell_name()})"
                self.get_input().get_log().get_logger().error(
                    f"{netlist.get_file_func_line_s(msg)}"
                )
                exit()

    def get_semiconductor_cell(self, inst_name, cell_name, cell_type):
        if netlist.Type.CELL_DIODE == cell_type:
            k_cells = [netlist.Type.CELL_DIODE]
            return self.get_cell_from_local_global(inst_name, cell_name, k_cells)
        elif netlist.Type.CELL_BJT == cell_type:
            k_cells = [netlist.Type.CELL_BJT_NPN, netlist.Type.CELL_BJT_PNP, netlist.Type.CELL_BJT]
            return self.get_cell_from_local_global(inst_name, cell_name, k_cells)
        elif netlist.Type.CELL_JFET == cell_type:
            k_cells = [
                netlist.Type.CELL_JFET_NJF,
                netlist.Type.CELL_JFET_PJF,
                netlist.Type.CELL_JFET,
            ]
            return self.get_cell_from_local_global(inst_name, cell_name, k_cells)
        elif netlist.Type.CELL_MOSFET == cell_type:
            k_cells = [
                netlist.Type.CELL_MOSFET_NMOS,
                netlist.Type.CELL_MOSFET_PMOS,
                netlist.Type.CELL_MOSFET,
            ]
            return self.get_cell_from_local_global(inst_name, cell_name, k_cells)
        else:
            msg = f"# error: model({cell_name}-{cell_type}) of inst({inst_name}) isnot exist!({self.get_cur_cell_name()})"
            self.get_input().get_log().get_logger().error(f"{netlist.get_file_func_line_s(msg)}")
            exit()

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
