import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

class mySizer(bt.Sizer):

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        margin = comminfo.margin
        mult = comminfo.params.mult
        #atr = self.strategy.atr[0]
        num_contracts = int(self.broker.getvalue() / margin / 20)
        print("buying" if isbuy else "selling",num_contracts)
        return num_contracts