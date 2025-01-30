#
import sys
import os
import logging
#
sys.path.append(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src')
import parser
import log
import makeiprobe
#
def MakeiprobeTest001():
    output_prefix   = 'MakeiprobeTest001'
    my_log          = log.Log(output_prefix)
    my_log.GetLogger().setLevel(logging.DEBUG)
    #
    my_makeiprobe   = makeiprobe.Makeiprobe(my_log)
    filename        = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc'
    #args            = f'makeiprobe {output_prefix} {filename} -net vdd vss vddq vssq -top_cell xxx -all_probe'
    #my_makeiprobe.Run(args.split())
    args            = f'makeiprobe {output_prefix} {filename} -net vdd vss vddq vssq'
    my_makeiprobe.Run(args.split())
#
if __name__ == '__main__':
    MakeiprobeTest001()