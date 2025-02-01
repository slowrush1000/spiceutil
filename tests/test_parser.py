import sys
import os
import logging

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import log
import parser


def test_parser_001():
    output_prefix = "test_parser_001"
    my_log = log.Log(output_prefix)
    my_log.get_logger().setLevel(logging.DEBUG)
    #
    my_parser = parser.Parser(my_log)
    my_filename = f"{os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))}/data/001.spc"
    my_parser.set_filename(my_filename)
    my_parser.run()
    #
    my_netlist = my_parser.get_netlist()
    my_output_filename = "2nd.spc"
    my_netlist.print_netlist(my_log.get_logger(), my_output_filename)


#
test_parser_001()
