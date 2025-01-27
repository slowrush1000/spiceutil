
import datetime
import argparse

#print(f'spiceutil.py makeiprobe -netlist spice_file -nets netname<...> -subckt_models subckt_model<...> <-top_cell top_cell_name> <-all_probe>')
class Makeiprobe(SpiceutilMode):
    def __init__(self):
        self.m_mode                 = Mode.MAKEIPROBE
        self.m_netnames             = []
        self.m_subckt_modelnames    = []
        self.m_all_probe            = False
        #
        self.m_arg_parser           = argparse.ArgumentParser()
    def ReadArgs(self, args):
        print(f'# read args start ... {datetime.datetime.now()}')
        self.m_arg_parser.add_argument('mode')
        self.m_arg_parser.add_argument('-netlist')
        self.m_arg_parser.add_argument('-net', action = 'append')
        self.m_arg_parser.add_argument('-subckt_model', action = 'append')
        self.m_arg_parser.add_argument('-top_cell')
        self.m_arg_parser.add_argument('-all_probe', action = 'store_true')
        args_value = self.m_arg_parser.parse_args() 
        self.m_netlist              = args_value.netlist
        self.m_netnames             = args_value.nets
        self.m_subckt_modelnames    = args_value.subckt_model
        self.m_
        print(f'# read args end ... {datetime.datetime.now()}')
    def SetAllProbeTrue(self):
        self.m_all_probe    = True
    def SetAllProbeFalse(self):
        self.m_all_probe    = False
    def PrintInputs(self):
        print(f'# print inputs start ... {datetime.datetime.now()}')
        print(f'    mode        : {self.GetMode()}')
        print(f'    netlist     : {self.m_netlist}')
        print(f'    nets        : {self.m_netnames}')
        print(f'    all probe   : {self.m_all_probe}')
        print(f'# print inputs end ... {datetime.datetime.now()}')
    def Run(self, args):
        print(f'# makeiprobe start ... {datetime.datetime.now()}')
        self.ReadArgs()
        self.PrintInputs()
        print(f'# makeiprobe end ... {datetime.datetime.now()}')