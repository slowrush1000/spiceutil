
import sys
import os
sys.path.append(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src')
import parser

def ParserTest001():
    my_parser   = parser.Parser()
    filename    = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/data/001.spc'
    my_parser.SetFilename(filename)
    my_parser.Run()

ParserTest001()