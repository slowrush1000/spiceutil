#
import datetime
from .spiceutil_parameters  import Parameters
from .spiceutil_utils       import k_TOP_CELLNAME
from .spiceutil_utils       import Type
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
    def PrintInfo(self, logger = None):
        logger.info(f'# logger.info info start ... {datetime.datetime.now()}')
        logger.info(f'key(name:::type) #inst #node #pin')
        for key in self.m_cell_dic:
            cell    = self.m_cell_dic[key]
            logger.info(f'{key} {len(cell.GetInstDic())} {len(cell.GetNodeDic())} {len(cell.GetPins())}')
        logger.info(f'# logger.info info end ... {datetime.datetime.now()}')
    def PrintNetlist(self, logger = None):
        if None == logger:
            print(f'# print netlist start ... {datetime.datetime.now()}')
            netlist_str     = ''
            for key in self.m_cell_dic:
                cell            = self.m_cell_dic[key]
                netlist_str     += cell.GetNetlistStr()
            print(f'{netlist_str}')
            print(f'# print netlist end ... {datetime.datetime.now()}')
        else:
            logger.info(f'# print netlist start ... {datetime.datetime.now()}')
            netlist_str     = ''
            for key in self.m_cell_dic:
                cell            = self.m_cell_dic[key]
                if k_TOP_CELLNAME() == cell.GetName():
                    continue
                netlist_str     += cell.GetNetlistStr()
            netlist_str         += '\n'
            k_top_cell_key      = self.GetCellKey(k_TOP_CELLNAME(), Type.CELL_CELL)
            if k_top_cell_key in self.m_cell_dic:
                cell            = self.m_cell_dic[k_top_cell_key]
                netlist_str     += cell.GetNetlistStr(False)
            logger.info(f'{netlist_str}')
            logger.info(f'# print netlist end ... {datetime.datetime.now()}')