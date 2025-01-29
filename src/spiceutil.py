
import sys
import datetime
import netlist
import log
import netlist
import parser
import makeiprobe

class Spiceutil:
    def PrintUsage(self):
        print(f'spiceutil.exe usage')
        print(f'spiceutil.py makeiprobe -o output_prefix -file spice_file -net netname<-net netname...> <-top_cell top_cell_name> <-all_probe>')
    def FindMode(self, args):
        if 2 > len(args):
            self.PrintUsage()
            exit()
        if 'makeiprobe' == args[1].lower():
            return netlist.Run.MAKEIPROBE
    def Run(self, args):
        print(f'# spiceutil.py start ... {datetime.datetime.now()}')
        if netlist.Run.MAKEIPROBE == self.FindMode(args):
            makeiprobe  = makeiprobe.Makeiprobe()
            makeiprobe.Run()
        print(f'# spiceutil.py end ... {datetime.datetime.now()}')
#
def main(args):
    my_spiceutil  = Spiceutil()
    my_spiceutil.Run(args)
#
if __name__ == '__main__':
    main(sys.argv)
