
import datetime
from spiceutil          import Spiceutil

class Makeiprobe(Spiceutil):
    def __init__(self):
        self.m_netnames             = []
        self.m_subckt_modelnames    = []
        self.m_all_probe            = False
    def ReadArgs(self, args):
        print(f' ')