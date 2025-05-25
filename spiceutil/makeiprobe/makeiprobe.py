import sys
import os
import inspect
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import version


class Makeiprobe:
    def __init__(self, t_input=None, t_log=None):
        self.__input = t_input
        self.__log = t_log
        self.__netlist = None

    def makeiprobe(self):
        self.__log.get_log().get_logger().info(
            f"# makeiprobe start ... {datetime.datetime.now()}"
        )
        top_cell = self.get_netlist().get_cell(
            self.__log.get_top_cellname(), utils.Type.CELL_CELL
        )
        if None == top_cell:
            self.__log.get_log().get_logger().info(
                f"# error : top cell({self.get_top_cellname()}) dont exist!"
            )
            self.__log.get_log().get_logger().info(
                f"# error : {self.makeiprobe.__name__}:{inspect.currentframe().f_lineno})"
            )
            exit()
        #
        for netname in self.__log.get_netnames():
            self.__log.get_log().get_logger().info(
                f"# makeiprobe({netname}) start ... { datetime.datetime.now()}"
            )
            probe_filename = f"{self.__log.get_output_prefix()}.{netname}.probe"
            self.__log.get_log().get_logger().info(f"probe file   : {probe_filename}")
            #
            probe_file = open(probe_filename, "wt")
            probe_file.write(
                f"* {version.Version().get_program()} - {version.Version().get_version()}\n"
            )
            probe_file.write(f"* {self.__log.get_run()} - {datetime.datetime.now()}\n")
            #
            self.makeiprobe_recursive(top_cell, probe_file, netname, "", 0)
            probe_file.write(f"*\n")
            probe_file.close()
            self.__log.get_log().get_logger().info(
                f"# make iprobe({netname}) end ... {
                datetime.datetime.now()}"
            )
        self.__log.get_log().get_logger().info(
            f"# make iprobe end ... {datetime.datetime.now()}"
        )

    def makeiprobe_recursive(
        self, parent_cell, probe_file, netname, parent_inst_name, level
    ):
        #
        k_subckt_type_nmos_pmos_mosfet = [
            utils.Type.CELL_CELL_NMOS,
            utils.Type.CELL_CELL_PMOS,
            utils.Type.CELL_NMOS,
            utils.Type.CELL_PMOS,
            utils.Type.CELL_MOSFET,
        ]
        k_subckt_type_nmos_pmos_mosfet_set = set(k_subckt_type_nmos_pmos_mosfet)
        #
        for inst_name in parent_cell.get_inst_dic():
            inst = parent_cell.get_inst_dic()[inst_name]
            #
            inst_name_1 = inst_name
            if 0 < level:
                inst_name_1 = f"{parent_inst_name}.{inst_name_1}"
            #
            cell = inst.get_cell()
            #
            if utils.Type.CELL_CELL == cell.get_type():
                self.makeiprobe_recursive(
                    cell, probe_file, netname, inst_name_1, level + 1
                )
            #
            else:
                node_size = inst.get_node_size()
                if False == self.__log.get_all_probe():
                    if cell.get_type() in k_subckt_type_nmos_pmos_mosfet_set:
                        node_size -= 1
                #
                for pos in range(0, node_size):
                    node = inst.get_node(pos)
                    if netname.lower() == node.get_name().lower():
                        # subckt model :
                        if cell.get_type() in utils.Utils().get_subckt_types_set():
                            self.write_iprobe_subckt_model(
                                probe_file, pos, inst_name_1, cell
                            )
                        else:
                            self.write_iprobe_normal_model(probe_file, pos, inst_name_1)

    def write_iprobe_normal_model(self, probe_file, pos, inst_name):
        probe_file.write(f".probe i{pos + 1}({inst_name})\n")

    def write_iprobe_subckt_model(self, probe_file, pos, inst_name, cell):
        probe_file.write(f".probe x({inst_name}.{cell.get_pins()[pos].get_name()})\n")

    def run(self, args=None):
        self.__log.get_log().get_logger().info(
            f"# makeiprobe start ... {datetime.datetime.now()}"
        )
        self.run_parser()
        self.makeiprobe()
        self.__log.get_log().get_logger().info(
            f"# makeiprobe end ... {datetime.datetime.now()}"
        )
