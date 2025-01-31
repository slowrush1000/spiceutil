#
import sys
import os
import logging
#
sys.path.append(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src')
import parser
import log
#
def ParserTest001():
    output_prefix   = 'ParserTest001'
    my_log          = log.Log(output_prefix)
    my_log.GetLogger().setLevel(logging.DEBUG)
    #
    my_parser   = parser.Parser(my_log)
    my_filename = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc'
    my_parser.SetFilename(my_filename)
    my_parser.Run()
    #
    my_netlist  = my_parser.GetNetlist()
    my_output_filename  = '2nd.spc'
    my_netlist.PrintNetlist(my_log.GetLogger(), my_output_filename)
#
ParserTest001()