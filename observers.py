import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue() # Get today's account value (cash + stocks)