#
import sys
import os
import logging
import unittest

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/src")
import netlist


class unittest_netlist(unittest.TestCase):
    def test_object(self):
        my_o = netlist.Object("aaa", netlist.Type.CELL_BJT)
        self.assertEqual(my_o.get_name(), "aaa")
        self.assertEqual(my_o.get_type(), netlist.Type.CELL_BJT)
        my_o.set_name("bbb")
        self.assertEqual(my_o.get_name(), "bbb")

    def test_netlist_split_cell_key(self):
        my_netlist = netlist.Netlist()
        cell_name = "ttt"
        cell_type = netlist.Type.CELL_BJT
        cell_key = my_netlist.get_cell_key(cell_name, cell_type)
        cell_name_1, cell_type_1 = my_netlist.split_cell_key(cell_key)
        self.assertEqual(cell_name, cell_name_1)
        self.assertEqual(cell_type, cell_type_1)


if __name__ == "__main__":
    unittest.main()
