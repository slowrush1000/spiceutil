
import sys
import datetime
import netlist
import parser
import makeiprobe

class Spiceutil:
    def PrintUsage(self):
        print(f'spiceutil.exe usage')
        print(f'spiceutil.py makeiprobe -netlist spice_file -nets netname<...> -subckt_model subckt_model<...> <-top_cell top_cell_name> <-all_probe>')
    def FindMode(self, args):
        if 2 > len(args):
            self.PrintUsage()
            exit()
        if 'makeiprobe' == args[1].lower():
            return netlist.Mode.MAKEIPROBE
    def Run(self, args):
        print(f'# spiceutil.py start ... {datetime.datetime.now()}')
#        if netlist.Mode.MAKEIPROBE == self.FindMode(args):
#            makeiprobe  = Makeiprobe()
#            makeiprobe.Run(args)
        print(f'# spiceutil.py end ... {datetime.datetime.now()}')

def main(args):
    my_spiceutil  = Spiceutil()
    my_spiceutil.Run(args)

if __name__ == '__main__':
    main(sys.argv)
