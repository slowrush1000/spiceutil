#
import sys
import os
import datetime
import inspect
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
#
class Parser(netlist.Netlist):
    def __init__(self, log = None):
        super().__init__()
        self.m_filename         = ''
        self.m_cur_cellname     = netlist.k_TOP_CELLNAME()
        self.m_cur_cell         = None
        self.m_casesensitive    = False
        self.m_dollar_comment   = True
        self.m_width            = 80
        #
        self.m_default_top_cell = self.GetCell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL)
        if None == self.m_default_top_cell:
            self.m_default_top_cell     = netlist.Cell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL)
            self.AddCell(netlist.k_TOP_CELLNAME(), self.m_default_top_cell, netlist.Type.CELL_CELL)
        #
        self.m_log              = log
    def SetFilename(self, filename):
        self.m_filename         = os.path.abspath(filename)
    def GetFilename(self):
        return self.m_filename
    def SetCurCell(self, cell):
        self.m_cur_cell     = cell
    def GetCurCell(self):
        return self.m_cur_cell
    def SetCurCellname(self, cellname):
        self.m_cur_cellname = cellname
    def GetCurCellname(self):
        return self.m_cur_cellname
    def GetDefaultTopCell(self):
        return self.m_default_top_cell
    def SetCasesensitive(self, casesensitive):
        self.m_casesensitive    = casesensitive
    def GetCasesensitive(self):
        return self.m_casesensitive
    def SetDollarComment(self, dollar_comment):
        self.m_dollar_comment   = dollar_comment
    def GetDollarComment(self):
        return self.m_dollar_comment
    def SetWidth(self, width):
        self.m_width = width
    def GetWidth(self):
        return self.m_width
    def SetLog(self, log):
        self.m_log  = log
    def GetLogger(self):
        return self.m_log
    def Read1st(self, filename):
        self.m_log.GetLogger().info(f'# read file({filename}) 1st start ... {datetime.datetime.now()}')
        nlines      = 0
        total_line  = ''
        with open(filename, 'rt') as f:
            while True:
                line    = f.readline()
                if not line:
                    break
                nlines  = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    log.info(f'    {nlines} lines ... {datetime.datetime.now()}')
                #
                if False == self.GetCasesensitive():
                    line    = line.lower()
                line    = line.lstrip().rstrip()
                line    = self.RemoveComment(line, self.GetDollarComment())
                if 0 == len(line):
                    continue
                #
                if '+' == line[0]:
                    total_line  = total_line + line[1:]
                else:
                    self.ReadTotalLine1st(total_line, filename)
                    total_line  = line
        self.ReadTotalLine1st(total_line, filename)
        self.m_log.GetLogger().info(f'    {nlines} lines ... {datetime.datetime.now()}')
        self.m_log.GetLogger().info(f'# read file({filename}) 1st end ... {datetime.datetime.now()}')
    def ReadTotalLine1st(self, total_line, filename):
        t_total_line    = total_line.replace('=', ' = ')
        tokens          = t_total_line.split()
        if 0 == len(tokens):
            return
        if '.subckt' == tokens[0].lower():
            self.ReadTotalLine1stSubcktLine(tokens)
        elif '.end' == tokens[0].lower():
            self.ReadTotalLine1stEndsLine(tokens)
        elif '.model' == tokens[0].lower():
            self.ReadTotalLine1stModelLine(tokens)
        elif ('.inc' == tokens[0].lower()) or ('.include' == tokens[0].lower()):
            self.ReadTotalLine1stIncludeLine(tokens, filename)
    def ReadTotalLine1stSubcktLine(self, tokens):
        name        = tokens[1]
        type        = netlist.Type.CELL_CELL
        if False == self.IsExistCell(name, type):
            cell    = netlist.Cell(name, type)
            self.SetCurCellname(name)
            self.AddCell(name, cell, type)
    def ReadTotalLine1stEndsLine(self):
        self.SetCurCellname(netlist.k_TOP_CELLNAME())
        self.SetCurCell(self.GetDefaultTopCell())
    def ReadTotalLine1stModelLine(self, tokens):
        name        = tokens[1].split('.')[0]
        type_name   = tokens[2]
        type        = netlist.Type.INIT
        if 'd' == type_name:
            type    = netlist.Type.CELL_DIODE
        elif 'npn' == type_name:
            type    = netlist.Type.CELL_NPN
        elif 'pnp' == type_name:
            type    = netlist.Type.CELL_PNP
        elif 'nmos' == type_name:
            type    = netlist.Type.CELL_NMOS
        elif 'pmos' == type_name:
            type    = netlist.Type.CELL_PMOS
        elif 'njf' == type_name:
            type    = netlist.Type.CELL_NJF
        elif 'pjf' == type_name:
            type    = netlist.Type.CELL_PJF
        #
        if False == self.IsExistCell(name, type):
            cell    = netlist.Cell(name, type)
            self.AddCell(name, cell, type)
    def ReadTotalLine1stIncludeLine(self, tokens, filename):
        t_filename  = tokens[1].replace('"', '').replace("'", "")
        # 절대경로 
        if '/' == t_filename[0]:
            self.Read1st(t_filename)
        # 상대경로
        else:
            absfilename = os.path.abspath(filename)
            absdirname  = os.path.dirname(absfilename)
            t_filename  = f'{absdirname}/{t_filename}'
            self.Read1st(t_filename)
    def Read2nd(self, filename):
        self.m_log.GetLogger().info(f'# read file({filename}) 2nd start ... {datetime.datetime.now()}')
        nlines      = 0
        total_line  = ''
        with open(filename, 'rt') as f:
            while True:
                line    = f.readline()
                if not line:
                    break
                nlines  = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    self.m_log.GetLogger().info(f'    {nlines} lines ... {datetime.datetime.now()}')
                #
                if False == self.GetCasesensitive():
                    line    = line.lower()
                line    = line.lstrip().rstrip()
                line    = self.RemoveComment(line, self.GetDollarComment())
                if 0 == len(line):
                    continue
                #
                if '+' == line[0]:
                    total_line  = total_line + line[1:]
                else:
                    self.ReadTotalLine2nd(total_line, filename)
                    total_line  = line
        self.ReadTotalLine2nd(total_line, filename)
        self.m_log.GetLogger().info(f'    {nlines} lines ... {datetime.datetime.now()}')
        self.m_log.GetLogger().info(f'# read file({filename}) 2nd end ... {datetime.datetime.now()}')
    def ReadTotalLine2nd(self, total_line, filename):
        t_total_line    = total_line.replace('=', ' = ')
        tokens          = t_total_line.split()
        if 0 == len(tokens):
            return
        if '.subckt' == tokens[0].lower():
            self.ReadTotalLine2ndSubcktLine(tokens)
        elif '.ends' == tokens[0].lower():
            self.ReadTotalLine1stEndsLine()
        elif '.model' == tokens[0].lower():
            pass
        elif '.inc' == tokens[0] or '.include' == tokens[0]:
            self.ReadTotalLine2ndIncludeLine(tokens, filename)
        elif 'r' == tokens[0][0]:
            self.ReadTotalLine2ndResistorLine(tokens)
        elif 'c' == tokens[0][0]:
            self.ReadTotalLine2ndCapacitorLine(tokens)
        elif 'l' == tokens[0][0]:
            self.ReadTotalLine2ndInductorLine(tokens)
        elif 'm' == tokens[0][0]:
            self.ReadTotalLine2ndMOSFETLine(tokens)
        elif 'q' == tokens[0][0]:
            self.ReadTotalLine2ndBJTLine(tokens)
        elif 'j' == tokens[0][0]:
            self.ReadTotalLine2ndJFETLine(tokens)
        elif 'd' == tokens[0][0]:
            self.ReadTotalLine2ndDiodeLine(tokens)
        elif 'x' == tokens[0][0]:
            self.ReadTotalLine2ndInstLine(tokens)
    def ReadTotalLine2ndSubcktLine(self, tokens):
        cell_name   = tokens[1]
        cell_type   = netlist.Type.CELL_CELL
        cell        = self.GetCell(cell_name, cell_type)
        if None == cell:
            self.m_log.GetLogger().info(f"# error : cell({cell_name}) dont exist!")
            self.m_log.GetLogger().info(f"# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        self.SetCurCell(cell)
        #
        parameter_start_pos     = self.GetParameterStartPos(tokens)
        #self.m_log.GetLogger().info(f'parameter_start_pos : {cell_name} - {parameter_start_pos}')
        if -1 == parameter_start_pos:
            parameter_start_pos = len(tokens)
        #
        for pos in range(2, parameter_start_pos):
            #self.m_log.GetLogger().debug(f'{cell_name} - {tokens[pos]}')
            pin_name    = tokens[pos]
            if False == cell.IsExistNode(pin_name):
                #self.m_log.GetLogger().debug(f'{cell_name} - {pin_name}')
                pin     = netlist.Node(pin_name, netlist.Type.NODE_PIN)
                cell.AddPin(pin_name, pin)
            else:
                line    = ' '.join(tokens)
                self.m_log.GetLogger().info(f'# error : cell({cell_name}) pin({pin_name}) is duplicate!')
                self.m_log.GetLogger().info(f'# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})')
                self.m_log.GetLogger().info(f'# error : {line}')
                exit()
        #
        cell.MakePinSet()
        #
        self.ReadParametersCell(cell, tokens, parameter_start_pos)
        #pins    = cell.GetPins()
        #for pin in pins:
        #    self.m_log.GetLogger().debug(f'{pin.GetName()}')
    def ReadTotalLine2ndIncludeLine(self, tokens, filename):
        t_filename  = tokens[1].replace('"', '').replace("'", "")
        # 절대경로 
        if '/' == t_filename[0]:
            self.Read1st(t_filename)
        # 상대경로
        else:
            absfilename = os.path.abspath(filename)
            absdirname  = os.path.dirname(absfilename)
            t_filename  = f'{absdirname}/{t_filename}'
            self.Read2nd(t_filename)
    def ReadTotalLine2ndResistorLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_R)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = self.GetParameterStartPos(tokens)
        cell_name               = netlist.GetDefaultRCell()
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name           = tokens[parameter_start_pos - 1]
        #self.m_log.GetLogger().debug(f'debug- {cell_name}')
        # rname n1 n2 value
        cell_type               = netlist.Type.CELL_R
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell    = netlist.Cell(cell_name, cell_type)
            self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 3):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        # rname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.ReadParametersInst(inst, tokens, parameter_start_pos)
        # rname n1 n2 value
        else:
            parameter_name      = netlist.GetDefaultRCell()
            parameter_equation  = tokens[3]
            inst.AddParameter(parameter_name, parameter_equation)
    # cname n1 n2 value
    def ReadTotalLine2ndCapacitorLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_C)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = self.GetParameterStartPos(tokens)
        cell_name               = netlist.GetDefaultCCell()
        # cname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name           = tokens[parameter_start_pos - 1]
        cell_type               = netlist.Type.CELL_C
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell    = netlist.Cell(cell_name, cell_type)
            self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 3):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.ReadParametersInst(inst, tokens, parameter_start_pos)
        else:
            parameter_name      = netlist.GetDefaultCCell()
            parameter_equation  = tokens[3]
            inst.AddParameter(parameter_name, parameter_equation)
    # lname n1 n2 value
    def ReadTotalLine2ndInductorLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_L)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {self.ReadTotalLine2ndInductorLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = self.GetParameterStartPos(tokens)
        cell_name               = netlist.GetDefaultLCell()
        # lname n1 n2 model r = value ...
        if 4 == parameter_start_pos and 4 < len(tokens):
            cell_name           = tokens[parameter_start_pos - 1]
        cell_type               = netlist.Type.CELL_L
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell    = netlist.Cell(cell_name, cell_type)
            self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 3):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        if 4 == parameter_start_pos and 4 < len(tokens):
            self.ReadParametersInst(inst, tokens, parameter_start_pos)
        else:
            parameter_name      = netlist.GetDefaultLCell()
            parameter_equation  = tokens[3]
            inst.AddParameter(parameter_name, parameter_equation)
    # mname n1 n2 n3 n4 cellname l = 100u w = 200u
    def ReadTotalLine2ndMOSFETLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_MOSFET)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {__file__}:{self.ReadTotalLine2ndMOSFETLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = 6
        cell_name               = tokens[5].lower()
        cell_type               = netlist.Type.CELL_NMOS
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell_type           = netlist.Type.CELL_PMOS
            cell                = self.GetCell(cell_name, cell_type)
            if None == cell:
                cell_type       = netlist.Type.CELL_MOSFET
                cell            = self.GetCell(cell_name, cell_type)
                if None == cell:
                    cell_type   = netlist.Type.CELL_MOSFET
                    cell        = netlist.Cell(cell_name, cell_type)
                    self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 5):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        self.ReadParametersInst(inst, tokens, parameter_start_pos)
    # qname n1 n2 n3 model ...
    def ReadTotalLine2ndBJTLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_BJT)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {__file__}:{self.ReadTotalLine2ndBJTLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = 5
        cell_name               = tokens[4].lower()
        cell_type               = netlist.Type.CELL_NPN
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell_type           = netlist.Type.CELL_PNP
            cell                = self.GetCell(cell_name, cell_type)
            if None == cell:
                cell_type       = netlist.Type.CELL_BJT
                cell            = self.GetCell(cell_name, cell_type)
                if None == cell:
                    cell_type   = netlist.Type.CELL_BJT
                    cell        = netlist.Cell(cell_name, cell_type)
                    self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 4):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        self.ReadParametersInst(inst, tokens, parameter_start_pos)
    # jname n1 n2 n3 model ...
    def ReadTotalLine2ndJFETLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_JFET)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {__file__}:{self.ReadTotalLine2ndJFETLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = 5
        cell_name               = tokens[4].lower()
        cell_type               = netlist.Type.CELL_JFET
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell_type           = netlist.Type.CELL_PJF
            cell                = self.GetCell(cell_name, cell_type)
            if None == cell:
                cell_type       = netlist.Type.CELL_NJF
                cell            = self.GetCell(cell_name, cell_type)
                if None == cell:
                    cell_type   = netlist.Type.CELL_JFET
                    cell        = netlist.Cell(cell_name, cell_type)
                    self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 4):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        self.ReadParametersInst(inst, tokens, parameter_start_pos)
    # dname n1 n2 model ...
    def ReadTotalLine2ndDiodeLine(self, tokens):
        inst_name       = tokens[0]
        inst            = self.GetCurCell().GetInst(inst_name)
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_DIODE)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {__file__}:{self.ReadTotalLine2ndDiodeLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = 4
        cell_name               = tokens[3].lower()
        cell_type               = netlist.Type.CELL_DIODE
        cell                    = self.GetCell(cell_name, cell_type)
        if None == cell:
            cell                = netlist.Cell(cell_name, cell_type)
            self.AddCell(cell_name, cell, cell_type)
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        #
        for pos in range(1, 3):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        self.ReadParametersInst(inst, tokens, parameter_start_pos)
    # xname n1 n2 ... cell ...
    def ReadTotalLine2ndInstLine(self, tokens):
        inst_name       = tokens[0]
        ## debug
        #print_debug     = False
        #if 'xc' == inst_name:
        #    print_debug     = True
        ##
        inst            = self.GetCurCell().GetInst(inst_name)
        #self.m_log.GetLogger().debug(f'debug - {inst_name} - {self.GetCurCell().GetName()}')
        if None == inst:
            inst        = netlist.Inst(inst_name, netlist.Type.INST_INST)
            self.GetCurCell().AddInst(inst_name, inst)
        else:
            self.m_log.GetLogger().info(f"# error : inst({inst_name}) is duplicate in cell({self.GetCurCellname()})")
            self.m_log.GetLogger().info(f"# error : {__file__}:{self.ReadTotalLine2ndInstLine.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        #
        parameter_start_pos     = self.GetParameterStartPos(tokens)
        cell_name               = tokens[parameter_start_pos - 1].lower()
        #self.m_log.GetLogger().debug(f'debug - inst {inst_name} cell {cell_name}')
        cell_type               = netlist.Type.CELL_CELL
        cell                    = self.GetCell(cell_name, cell_type)
        ## debug
        #if True == print_debug:
        #    self.m_log.GetLogger().debug(f'inst {inst_name} cell {cell_name}')
        ##
        if None == cell:
            cell                = netlist.Cell(cell_name, cell_type)
            self.AddCell(cell_name, cell, cell_type)
            #self.m_log.GetLogger().debug(f'debug - 00 inst {inst_name} cell {cell_name}')
        ## debug
        #if True == print_debug:
        #    self.m_log.GetLogger().debug(f'cell {cell.GetNetlistStr()}')
        ##
        inst.SetCell(cell)
        cell.IncreaseInstSize()
        ## debug
        #if True == print_debug:
        #    self.m_log.GetLogger().debug(f'inst {inst.GetNetlistStr()} {inst.GetCell().GetName()}')
        ##
        for pos in range(1, parameter_start_pos - 1):
            node_name   = tokens[pos]
            node        = self.GetCurCell().GetNode(node_name)
            if None == node:
                node    = netlist.Node(node_name, netlist.Type.NODE_NODE)
                self.GetCurCell().AddNode(node_name, node)
            inst.AddNode(node)
            node.AddInst(inst_name, inst)
        #
        self.ReadParametersInst(inst, tokens, parameter_start_pos)
    def GetParameterStartPos(self, tokens):
        parameter_start_pos = len(tokens)
        for pos in range(1, len(tokens)):
            if '=' == tokens[pos]:
                parameter_start_pos = pos - 1
                break
        return parameter_start_pos
    # *...
    # $...
    # ... name='equation*equation" * comments
    def RemoveComment(self, line, dollar_comment = True):
        t_line              = line
        t_line              = t_line.replace('"', "'")
        #print(f'001 {t_line}')
        # $
        if True == dollar_comment:
            dollar_pos      = t_line.find('$')
            if -1 != dollar_pos:
                t_line      = t_line[:dollar_pos]
        #print(f'002 {t_line}')
        # *
        quatation_pos       = t_line.rfind("'")
        #print(f'003 {quatation_pos}')
        if -1 == quatation_pos:
            star_pos        = t_line.find("*")
            #print(f'004 {star_pos}')
            if -1 == star_pos:
                return t_line
            else:
                return t_line[:star_pos]
        else:
            star_pos        = t_line.find("*", quatation_pos)
            #print(f'005 {star_pos}')
            if -1 == star_pos:
                return t_line
            else:
                return t_line[:star_pos]
    def ReadParametersCell(self, cell, tokens, parameter_start_pos):
        name_pos                = parameter_start_pos
        equation_start_pos      = len(tokens) 
        equation_end_pos        = len(tokens)
        for pos in range(len(tokens) - 1, parameter_start_pos, -1):
            if '=' == tokens[pos]:
                name_pos            = pos - 1
                equation_start_pos  = pos + 1
                #self.m_log.GetLogger().debug(f'debug : pos : {pos} name_pos : {name_pos} equation_start_pos : {equation_start_pos} equation_end_pos : {equation_end_pos}')
                name                = tokens[name_pos]
                equation            = ' '.join(tokens[equation_start_pos:equation_end_pos])
                equation            = equation.replace(' ', '').replace('\t', '').replace("'", "").replace('"', '')
                cell.AddParameter(name, equation)
                equation_end_pos    = name_pos
    def ReadParametersInst(self, inst, tokens, parameter_start_pos):
        name_pos                = parameter_start_pos
        equation_start_pos      = len(tokens) 
        equation_end_pos        = len(tokens)
        for pos in range(len(tokens) - 1, parameter_start_pos, -1):
            if '=' == tokens[pos]:
                name_pos            = pos - 1
                equation_start_pos  = pos + 1
                name                = tokens[name_pos]
                equation            = ' '.join(tokens[equation_start_pos:equation_end_pos])
                equation            = equation.replace(' ', '').replace('\t', '').replace("'", "").replace('"', '')
                inst.AddParameter(name, equation)
                equation_end_pos    = name_pos
    def Run(self):
        self.m_log.GetLogger().info(f'# read file({self.m_filename}) start ... {datetime.datetime.now()}')
        self.Read1st(self.GetFilename())
        self.PrintInfo(self.m_log.GetLogger())
        self.PrintNetlist(self.m_log.GetLogger())
        self.PrintNetlist(self.m_log.GetLogger(), '1st.spc', self.GetWidth())
        self.Read2nd(self.GetFilename())
        self.PrintInfo(self.m_log.GetLogger())
        self.PrintNetlist(self.m_log.GetLogger())
        self.PrintNetlist(self.m_log.GetLogger(), '2nd.spc', self.GetWidth())
        self.m_log.GetLogger().info(f'# read file({self.m_filename}) end ... {datetime.datetime.now()}')
#
def TestGetParameterStartPos():
    my_parser   = Parser()
    tokens      = [ 'r1', 'n1', 'n2', 'l', '=', '100u', 'w', '=', '200u']
    parameter_start_pos     = my_parser.GetParameterStartPos(tokens)
    print(f'{parameter_start_pos}')
#
def TestRemoveComment():
    my_parser   = Parser()
    line        =   "xname n1 n2 cell l='1*100' "
    line        +=  'w="200*300" * comments'
    lines       = []
    lines.append(line)
    line        =   "* comment"
    lines.append(line)
    line        =   "r1 n1 n2 1000 $comment"
    lines.append(line)
    line        =   "$comment"
    lines.append(line)
    line        =   "xname n1 n2 cell $comment"
    lines.append(line)
    line        =   "xname n1 n2 cell $comment"
    lines.append(line)
    line        =   ".subckt a 1 2 l=100u w=200u $ aaa"
    lines.append(line)
    for line in lines:
        print(f'before : {line}')
        print(f'after  : {my_parser.RemoveComment(line)}')
#
if __name__ == '__main__':
    #TestGetParameterStartPos()
    TestRemoveComment()