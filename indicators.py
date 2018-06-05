import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math
import evwap
class TrendStrength(bt.Indicator):

    lines = ('strength',)
    params = (('periods',[5,10,20,30,40,50]),)

    plotinfo = dict(subplot=True)
    plotlines = dict(
        strength=dict(ls='--'),
    )

    def __init__(self):
        self.addminperiod(max(self.params.periods))
        self.ma = []
        for p in self.params.periods:
            self.ma.append(bt.ind.EMA(period=p))

    def next(self):
        above = 0
        max_above = sum(range(len(self.ma)))
        for i,ma in enumerate(self.ma):
            for test_ma in self.ma[i+1:]:
                if ma[0] > test_ma[0]:
                    above +=1
        strength = ((above / max_above) - .5) *2
        if math.isnan(strength):
            strength = 0
        self.lines.strength[0] = strength