
import sys
import datetime
from spiceutil_type         import Mode
from spiceutil_makeiprobe   import Makeiprobe
from spiceutil_netlist      import Netlist


class Spiceutil:
    def __init__(self):
        self.m_netlist  = Netlist()
        #
        self.m_spice_filename   = ''
        self.m_mode             = Mode.MAKE_I_PROBE
    def PrintUsage(self):
        print(f'spiceutil.exe usage')
        print(f'spiceutil.py makeiprobe -netlist spice_file -nets netname<...> -subckt_model subckt_model<...> -all_probe')
    def ReadArgs(self):
    def Run(self, args):
        print(f'# spiceutil.py start ... {datetime.datetime.now()}')
        print(f'# spiceutil.py end ... {datetime.datetime.now()}')

def main(args):
    my_spiceutil  = Spiceutil()
    my_spiceutil.Run(args)

if __name__ == '__main__':
    main(sys.argv)
