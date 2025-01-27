
#
import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
#
class Parser(netlist.Netlist):
    def __init__(self):
        super().__init__()
        self.m_filename         = ''
        self.m_cur_cellname     = netlist.k_TOP_CELLNAME()
        self.m_cur_cell         = None
        #
        self.m_default_top_cell = None
        if False == self.IsExistCell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL):
            default_cell            = netlist.Cell(netlist.k_TOP_CELLNAME(), netlist.Type.CELL_CELL)
            self.m_default_top_cell = default_cell
    def SetFilename(self, filename):
        self.m_filename         = os.path.abspath(filename)
    def GetFilename(self):
        return self.m_filename
    def Read1st(self, filename):
        print(f'# read file({filename}) 1st start ... {datetime.datetime.now()}')
        nlines      = 0
        total_line  = ''
        with open(filename, 'rt') as f:
            while True:
                line    = f.readline()
                if not line:
                    break
                nlines  = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    print(f'    {nlines} lines ... {datetime.datetime.now()}')
                #
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
        print(f'    {nlines} lines ... {datetime.datetime.now()}')
        print(f'# read file({filename}) 1st end ... {datetime.datetime.now()}')
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
        elif '.inc' == tokens[0] or '.include' == tokens[0]:
            self.ReadTotalLine1stIncludeLine(tokens, filename)
    def ReadTotalLine1stSubcktLine(self, tokens):
        name        = tokens[1]
        type        = netlist.Type.CELL_CELL
        if False == self.IsExistCell(name, type):
            cell                    = netlist.Cell(name, type)
            #
            self.m_cur_cellname     = name
            #
            self.AddCell(name, cell, type)
    def ReadTotalLine1stEndsLine(self, tokens):
        self.m_cur_cellname         = netlist.k_TOP_CELLNAME
        self.m_cur_cell             = self.m_default_top_cell
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
            cell                    = netlist.Cell(name, type)
            #
            self.m_cur_cellname     = name
            #
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
        print(f'# read file({filename}) 2nd start ... {datetime.datetime.now()}')
        nlines      = 0
        total_line  = ''
        with open(filename, 'rt') as f:
            while True:
                line    = f.readline()
                if not line:
                    break
                nlines  = nlines + 1
                if 0 == (nlines % netlist.k_LINE_STEP()):
                    print(f'    {nlines} lines ... {datetime.datetime.now()}')
                #
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
        print(f'    {nlines} lines ... {datetime.datetime.now()}')
        print(f'# read file({filename}) 2nd end ... {datetime.datetime.now()}')
    def ReadTotalLine2nd(self, total_line, filename):
        t_total_line    = total_line.replace('=', ' = ')
        tokens          = t_total_line.split()
        if 0 == len(tokens):
            return
        if '.subckt' == tokens[0].lower():
            name        = tokens[1]
            type        = netlist.Type.CELL_CELL
            if False == self.IsExistCell(name, type):
                cell                    = netlist.Cell(name, type)
                #
                self.m_cur_cellname     = name
                #
                self.AddCell(name, cell, type)
        elif '.end' == tokens[0].lower():
            self.m_cur_cellname         = netlist.k_TOP_CELLNAME
            self.m_cur_cell             = self.m_default_top_cell
        elif '.model' == tokens[0].lower():
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
                cell                    = netlist.Cell(name, type)
                #
                self.m_cur_cellname     = name
                #
                self.AddCell(name, cell, type)
        elif '.inc' == tokens[0] or '.include' == tokens[0]:
            t_filename  = tokens[1].replace('"', '').replace("'", "")
            # 절대경로 
            if '/' == t_filename[0]:
                self.Read2nd(t_filename)
            # 상대경로
            else:
                absfilename = os.path.abspath(filename)
                absdirname  = os.path.dirname(absfilename)
                t_filename  = f'{absdirname}/{t_filename}'
                self.Read2nd(t_filename)
    def Run(self):
        print(f'# read file({self.m_filename}) start ... {datetime.datetime.now()}')
        self.Read1st(self.GetFilename())
        self.PrintInfo()
        #self.Read2nd(self.m_filename)
        print(f'# read file({self.m_filename}) end ... {datetime.datetime.now()}')