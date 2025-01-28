
import sys
import os
sys.path.append(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src')
import parser
import log

def ParserTest001():
    output_prefix   = 'ParserTest001'
    my_log          = log.Log(output_prefix)
    #
    my_parser   = parser.Parser(my_log)
    filename    = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc'
    my_parser.SetFilename(filename)
    my_parser.Run()

ParserTest001()