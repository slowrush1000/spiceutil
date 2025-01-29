#
import sys
import datetime
import logging
#
import log
import makeiprobe
import netlist
import parser
#
class Spiceutil:
    def PrintUsage(self):
        print(f'spiceutil.exe usage')
        print(f'spiceutil.py makeiprobe output_prefix filename -net netname<...> <-top_cell top_cell_name> <-all_probe>')
    def GetRunOutputPrefix(self, args):
        if 3 > len(args):
            self.PrintUsage()
            exit()
        output_prefix   = args[2]
        if 'makeiprobe' == args[1].lower():
            return [ netlist.Run.MAKEIPROBE, output_prefix ]
    def Run(self, args):
        print(f'# spiceutil.py start ... {datetime.datetime.now()}')
        run_output_prefix   = self.GetRunOutputPrefix(args)
        if netlist.Run.MAKEIPROBE == run_output_prefix[0]:
            output_prefix   = run_output_prefix[1]
            my_log          = log.Log(output_prefix)
            my_log.GetLogger().setLevel(logging.DEBUG)
            makeiprobe  = makeiprobe.Makeiprobe(my_log)
            makeiprobe.Run()
        print(f'# spiceutil.py end ... {datetime.datetime.now()}')
#
def main(args):
    my_spiceutil  = Spiceutil()
    my_spiceutil.Run(args)
#
if __name__ == '__main__':
    main(sys.argv)
