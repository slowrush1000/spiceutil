#
import datetime
import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import netlist
import log
import parser
#
class Makeiprobe(netlist.Netlist):
    def __init__(self):
        self.m_run                  = netlist.Run.MAKEIPROBE
        self.m_output_prefix        = ''
        self.m_filename             = ''
        self.m_netnames             = []
        self.m_top_cellname         = netlist.k_TOP_CELLNAME()
        self.m_all_probe            = False
        #
        self.m_log                  = None
        #
        self.m_arg_parser           = argparse.ArgumentParser()
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
    def ReadArgs(self):
        print(f'# read args start ... {datetime.datetime.now()}')
        #
        self.m_arg_parser.add_argument('run')
        self.m_arg_parser.add_argument('-o', '--output_prefix')
        self.m_arg_parser.add_argument('-f', '--file')
        self.m_arg_parser.add_argument('-n', '--net', action = 'append')
        self.m_arg_parser.add_argument('-top_cell')
        self.m_arg_parser.add_argument('-all_probe', action = 'store_true')
        #
        args    = self.m_arg_parser.parse_args() 
        self.SetOutputPrefix(args.output_prefix)
        self.SetFilename(args.file)
        self.SetNetnames(args.net.split())
        self.SetTopCellname(args.top_cell)
        self.SetAllProbe(args.all_probe)
        print(f'# read args end ... {datetime.datetime.now()}')
    def PrintInputs(self):
        self.GetLog().GetLogger().info(f'# print inputs start ... {datetime.datetime.now()}')
        self.GetLog().GetLogger().info(f'    run            : {self.GetRun()}')
        self.GetLog().GetLogger().info(f'    output_prefix  : {self.GetOutputPrefix()}')
        self.GetLog().GetLogger().info(f'    file           : {self.GetFilename()}')
        for netname in self.GetNetnames():
            self.GetLog().GetLogger().info(f'    net            : {netname}')
        self.GetLog().GetLogger().info(f'    top[ cell      : {self.GetTopCellname()}]')
        self.GetLog().GetLogger().info(f'    all probe      : {self.GetAllProbe}')
        self.GetLog().GetLogger().info(f'# print inputs end ... {datetime.datetime.now()}')
    def Run(self):
        self.GetLog().GetLogger().info(f'# makeiprobe start ... {datetime.datetime.now()}')
        self.ReadArgs()
        self.PrintInputs()
        self.GetLog().GetLogger().info(f'# makeiprobe end ... {datetime.datetime.now()}')