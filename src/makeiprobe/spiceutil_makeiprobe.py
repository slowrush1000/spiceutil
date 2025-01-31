#
import datetime
import argparse
import sys
import os
import inspect
#
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import parser
#
class Makeiprobe(netlist.Netlist):
    def __init__(self, log = None):
        self.m_run                  = netlist.Run.MAKEIPROBE
        self.m_output_prefix        = ''
        self.m_filename             = ''
        self.m_netnames             = []
        self.m_top_cellname         = netlist.k_TOP_CELLNAME()
        self.m_all_probe            = False
        #
        self.m_log                  = log
        #
        self.m_arg_parser           = argparse.ArgumentParser()
        self.m_netlist              = None
    def SetLog(self, log):
        self.m_log  = log
    def GetLog(self):
        return self.m_log
    def SetRun(self, run):
        self.m_run  = run
    def GetRun(self):
        return self.m_run
    def SetOutputPrefix(self, output_prefix):
        self.m_output_prefix             = output_prefix
    def GetOutputPrefix(self):
        return self.m_output_prefix
    def SetFilename(self, filename):
        self.m_filename             = filename
    def GetFilename(self):
        return self.m_filename
    def SetNetnames(self, netnames):
        self.m_netnames = netnames
    def GetNetnames(self):
        return self.m_netnames
    def SetTopCellname(self, top_cellname):
        self.m_top_cellname     = top_cellname
    def GetTopCellname(self):
        return self.m_top_cellname
    def SetAllProbe(self, all_probe):
        self.m_all_probe    = all_probe
    def GetAllProbe(self):
        return self.m_all_probe
    def SetNetlist(self, netlist):
        self.m_netlist  = netlist
    def GetNetlist(self):
        return self.m_netlist
    def ReadArgs(self, args = None):
        self.GetLog().GetLogger().info(f'# read args start ... {datetime.datetime.now()}')
        #
        self.m_arg_parser.add_argument('run')
        self.m_arg_parser.add_argument('output_prefix')
        self.m_arg_parser.add_argument('filename')
        self.m_arg_parser.add_argument('-net', action = 'extend', nargs = '+', type = str)
        self.m_arg_parser.add_argument('-top_cell', default = netlist.k_TOP_CELLNAME())
        self.m_arg_parser.add_argument('-all_probe', action = 'store_true', default = False)
        #
        args_1      = None
        if None == args:
            args_1  = self.m_arg_parser.parse_args()
        else:
            args_1  = self.m_arg_parser.parse_args(args)
        self.SetOutputPrefix(args_1.output_prefix)
        self.SetFilename(args_1.filename)
        self.SetNetnames(args_1.net)
        self.SetTopCellname(args_1.top_cell)
        self.SetAllProbe(args_1.all_probe)
        self.GetLog().GetLogger().info(f'# read args end ... {datetime.datetime.now()}')
    def PrintInputs(self):
        self.GetLog().GetLogger().info(f'# print inputs start ... {datetime.datetime.now()}')
        self.GetLog().GetLogger().info(f'    run            : {self.GetRun()}')
        self.GetLog().GetLogger().info(f'    output_prefix  : {self.GetOutputPrefix()}')
        self.GetLog().GetLogger().info(f'    file           : {self.GetFilename()}')
        for netname in self.GetNetnames():
            self.GetLog().GetLogger().info(f'    net            : {netname}')
        self.GetLog().GetLogger().info(f'    top cell       : {self.GetTopCellname()}')
        self.GetLog().GetLogger().info(f'    all probe      : {self.GetAllProbe()}')
        self.GetLog().GetLogger().info(f'# print inputs end ... {datetime.datetime.now()}')
    def RunParser(self):
        my_parser   = parser.Parser(self.GetLog())
        my_parser.SetFilename(self.GetFilename())
        my_parser.Run()
        self.SetNetlist(my_parser.GetNetlist())
    def MakeIprobe(self):
        self.GetLog().GetLogger().info(f'# make iprobe start ... {datetime.datetime.now()}')
        top_cell    = self.GetNetlist().GetCell(self.GetTopCellname(), netlist.Type.CELL_CELL)
        if None == top_cell:
            self.m_log.GetLogger().info(f"# error : top cell({self.GetTopCellname()}) dont exist!")
            self.m_log.GetLogger().info(f"# error : {self.MakeIprobe.__name__}:{inspect.currentframe().f_lineno})")
            exit()
        for netname in self.GetNetnames():
            self.m_log.GetLogger().info(f'# make iprobe({netname}) start ... {datetime.datetime.now()}')
            probe_filename  = f'{self.GetOutputPrefix()}.{netname}.probe'
            self.m_log.GetLogger().info(f'    probe file : {probe_filename}')
            #
            probe_file      = open(probe_filename, 'wt')
            probe_file.write(f'* {netlist.GetProgram()} - {netlist.GetVersion()}\n')
            probe_file.write(f'* {datetime.datetime.now()}\n')
            #
            self.MakeIprobeRecursive(top_cell, probe_file, netname, '', 0)
            probe_file.write(f'*\n')
            probe_file.close()
            self.m_log.GetLogger().info(f'# make iprobe({netname}) end ... {datetime.datetime.now()}')
        self.GetLog().GetLogger().info(f'# make iprobe end ... {datetime.datetime.now()}')
    def MakeIprobeRecursive(self, parent_cell, probe_file, netname, parent_inst_name, level):
        for inst_name in parent_cell.GetInstDic():
            inst    = parent_cell.GetInstDic()[inst_name]
            #
            inst_name_1 = inst_name
            if 0 < level:
                inst_name_1     = f'{parent_inst_name}.{inst_name_1}'
            #self.GetLog().GetLogger().info(f'debug- lvl({level}) inst({inst_name_1})')
            cell    = inst.GetCell()
            if netlist.Type.CELL_CELL == cell.GetType():
                self.MakeIprobeRecursive(cell, probe_file, netname, inst_name_1, level + 1)
            else:
                if True == self.GetAllProbe():
                    for pos in range(0, inst.GetNodeSize()):
                        node    = inst.GetNode(pos)
                        if netname.lower() == node.GetName().lower():
                            probe_file.write(f'.probe i{pos + 1}({inst_name_1})\n')
                else:
                    node_size   = inst.GetNodeSize()
                    if (netlist.Type.CELL_MOSFET == cell.GetType()) or (netlist.Type.CELL_NMOS == cell.GetType()) or (netlist.Type.CELL_PMOS == cell.GetType()):
                        node_size   -= 1
                    for pos in range(0, node_size):
                        node    = inst.GetNode(pos)
                        if netname.lower() == node.GetName().lower():
                            probe_file.write(f'.probe i{pos + 1}({inst_name_1})\n')
    def Run(self, args = None):
        self.GetLog().GetLogger().info(f'# makeiprobe start ... {datetime.datetime.now()}')
        self.ReadArgs(args)
        self.PrintInputs()
        self.RunParser()
        self.MakeIprobe()
        self.GetLog().GetLogger().info(f'# makeiprobe end ... {datetime.datetime.now()}')