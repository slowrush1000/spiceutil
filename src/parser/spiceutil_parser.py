
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
        #
        self.m_default_top_cell = None
        if False == self.IsExistCell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL):
            default_cell            = netlist.Cell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL)
            self.m_default_top_cell = default_cell
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
                if 0 == len(line):
                    continue
                #
                if ('*' == line[0]) or ('$' == line[0]):
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
    def ReadTotalLine1stEndsLine(self, tokens):
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
                if 0 == len(line):
                    continue
                #
                if ('*' == line[0]) or ('$' == line[0]):
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
        elif '.end' == tokens[0].lower():
            self.ReadTotalLine1stEndsLine()
        elif '.model' == tokens[0].lower():
            pass
        elif '.inc' == tokens[0] or '.include' == tokens[0]:
            self.ReadTotalLine2ndIncludeLine(tokens, filename)
        elif 'r' == tokens[0][0]:
            pass
        elif 'c' == tokens[0][0]:
            pass
        elif 'l' == tokens[0][0]:
            pass
        elif 'm' == tokens[0][0]:
            pass
        elif 'q' == tokens[0][0]:
            pass
        elif 'j' == tokens[0][0]:
            pass
        elif 'x' == tokens[0][0]:
            pass
    def ReadTotalLine2ndSubcktLine(self, tokens):
        name        = tokens[1]
        type        = netlist.Type.CELL_CELL
        cell        = self.GetCell(name, type)
        if None == cell:
            line    = ' '.join(tokens)
            self.m_log.GetLogger().info(f"# error : cell({name}) dont exist!")
            self.m_log.GetLogger().info(f"# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})")
            self.m_log.GetLogger().info(f'# error : {line}')
            exit()
        self.SetCurCell(cell)
        for pos in range(2, len(tokens)):
            self.m_log.GetLogger().info(f'debug-000 {name} - {tokens[pos]}')
            if False == cell.IsExistNode(tokens[pos]):
                self.m_log.GetLogger().info(f'debug-001 {name} - {tokens[pos]}')
                pin     = netlist.Node(tokens[pos], netlist.Type.NODE_PIN)
                cell.AddPin(tokens[pos], pin)
            else:
                line    = ' '.join(tokens)
                self.m_log.GetLogger().info(f'# error : cell({name}) pin({tokens[pos]}) is duplicate!')
                self.m_log.GetLogger().info(f'# error : {self.ReadTotalLine2ndSubcktLine.__name__}:{inspect.currentframe().f_lineno})')
                self.m_log.GetLogger().info(f'# error : {line}')
                exit()
        pins    = cell.GetPins()
        for pin in pins:
            self.m_log.GetLogger().info(f'debug-111 {pin.GetName()}')
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
    # rname n1 n2 value
    # rname n1 n2 model r=value ...
    def ReadTotalLine2ndRLine(self, tokens):
        name            = tokens[0]
        inst            = self.m_cur_cell.GetInst(name)
        if None == inst:
            inst        = netlist.Inst(name, netlist.Type.INST_R)
            cell        = self.Get
        for pos in range(1, 3):
            node        = self.m_cur_cell.GetNode(tokens[pos])
            if None == node:
                node    = netlist.Node(name, netlist.Type.INST_R)
    #def ReadTotalLine2ndMOSFETLine(self, tokens):
    # xname n1 n2 ... nN cellname l    =    100u w    =    200u
    # 0     1  2  ... N  N+1      N+2  N+3  N+4  N+5  N+6  N+7
    def FindParameterStartPos(self, tokens):
        parameter_start_pos = -1
        for pos in range(len(tokens) - 1, 1, -1):
            if '=' == tokens[pos]:
                parameter_start_pos = pos
                break
        return parameter_start_pos
    def Run(self):
        self.m_log.GetLogger().info(f'# read file({self.m_filename}) start ... {datetime.datetime.now()}')
        self.Read1st(self.GetFilename())
        self.PrintInfo()
        self.PrintNetlist()
        self.Read2nd(self.GetFilename())
        self.PrintNetlist()
        self.m_log.GetLogger().info(f'# read file({self.m_filename}) end ... {datetime.datetime.now()}')