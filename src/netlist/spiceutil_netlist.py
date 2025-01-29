#
import datetime
import textwrap
from .spiceutil_parameters  import Parameters
from .spiceutil_utils       import k_TOP_CELLNAME
from .spiceutil_utils       import Type
from .spiceutil_utils       import GetProgram
from .spiceutil_utils       import GetVersion
#
class Netlist(Parameters):
    def __init__(self):
        super().__init__()
        self.m_cell_dic = {}
        self.m_top_cellname = k_TOP_CELLNAME
        self.m_top_cell = None
    def SetTopCellname(self, top_cellname):
        self.m_top_cellname = top_cellname
    def GetTopCellname(self):
        return self.m_top_cellname
    def SetTopCell(self, top_cell):
        self.m_top_cell = top_cell
    def GetTopCell(self):
        return self.m_top_cell
    def GetCellDic(self):
        return self.m_cell_dic
    def IsExistCell(self, name, type):
        key     = self.GetCellKey(name, type)
        if key in self.m_cell_dic:
            return True
        else:
            return False
    def GetCell(self, name, type):
        key     = self.GetCellKey(name, type)
        if key in self.m_cell_dic:
            return self.m_cell_dic[key]
        else:
            return None
    def AddCell(self, name, cell, type):
        key     = self.GetCellKey(name, type)
        if not key in self.m_cell_dic:
            self.m_cell_dic[key]   = cell
    def GetCellKey(self, name, type):
        return f'{name}:::{type}'
    def GetInfoStr(self):
        info_str        = ''
        info_str        += f'key(name:::type) #inst #node #pin #inst\n'
        for key in self.m_cell_dic:
            cell        = self.m_cell_dic[key]
            info_str    += f'{key} {len(cell.GetInstDic())} {len(cell.GetNodeDic())} {len(cell.GetPins())} {cell.GetInstSize()}\n'
        return info_str
    def PrintInfo(self, logger = None):
        if None == logger:
            print(f'# print info start ... {datetime.datetime.now()}')
            print(f'{self.GetInfoStr()}')
            print(f'# print info end ... {datetime.datetime.now()}')
        else:
            logger.info(f'# print info start ... {datetime.datetime.now()}')
            logger.info(f'{self.GetInfoStr()}')
            logger.info(f'# print info end ... {datetime.datetime.now()}')
    def GetNetlistStr(self):
        netlist_str     = []
        #
        for key in self.m_cell_dic:
            cell            = self.m_cell_dic[key]
            if k_TOP_CELLNAME() == cell.GetName():
                continue
            netlist_str     += cell.GetNetlistStr()
        #
        k_top_cell_key      = self.GetCellKey(k_TOP_CELLNAME(), Type.CELL_CELL)
        if k_top_cell_key in self.m_cell_dic:
            cell            = self.m_cell_dic[k_top_cell_key]
            netlist_str     += cell.GetNetlistStr(False)
        #
        return netlist_str
    def PrintNetlist(self, logger = None, filename = None, width = 120):
        if (None == logger) and (None == filename):
            print(f'# print netlist start ... {datetime.datetime.now()}')
            for netlist_line in self.GetNetlistStr():
                wrap_netlist_lines = textwrap.wrap(netlist_line, width = width, subsequent_indent = '+ ', break_long_words = False, break_on_hyphens = False)
                for wrap_netlist_line in wrap_netlist_lines:
                    print(f'{wrap_netlist_line}')
            print(f'# print netlist end ... {datetime.datetime.now()}')
        elif (None == logger) and (None != filename):
            print(f'# print netlist start ... {datetime.datetime.now()}')
            print(f'netlist file : {filename}')
            f = open(filename, 'wt')
            for netlist_line in self.GetNetlistStr():
                wrap_netlist_lines = textwrap.wrap(netlist_line, width = width, subsequent_indent = '+ ', break_long_words = False, break_on_hyphens = False)
                for wrap_netlist_line in wrap_netlist_lines:
                    f.write(f'{wrap_netlist_line}\n')
            f.close()
            print(f'# print netlist end ... {datetime.datetime.now()}')
        elif (None != logger) and (None == filename):
            logger.info(f'# print netlist start ... {datetime.datetime.now()}')
            for netlist_line in self.GetNetlistStr():
                wrap_netlist_lines = textwrap.wrap(netlist_line, width = width, subsequent_indent = '+ ', break_long_words = False, break_on_hyphens = False)
                for wrap_netlist_line in wrap_netlist_lines:
                    logger.info(f'{wrap_netlist_line}')
            logger.info(f'# print netlist end ... {datetime.datetime.now()}')
        elif (None != logger) and (None != filename):
            logger.info(f'# print netlist start ... {datetime.datetime.now()}')
            logger.info(f'netlist file : {filename}')
            f = open(filename, 'wt')
            for netlist_line in self.GetNetlistStr():
                wrap_netlist_lines = textwrap.wrap(netlist_line, width = width, subsequent_indent = '+ ', break_long_words = False, break_on_hyphens = False)
                for wrap_netlist_line in wrap_netlist_lines:
                    f.write(f'{wrap_netlist_line}\n')
            f.close()
            logger.info(f'# print netlist end ... {datetime.datetime.now()}')