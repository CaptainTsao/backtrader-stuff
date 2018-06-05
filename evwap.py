import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

class EVWAP(bt.Indicator):

    lines = ('evwap',)
    params = (('period',10),)

    plotinfo = dict(subplot=False)
    plotlines = dict(
        evwap=dict(ls='--'),
    )

    def __init__(self):
        self.addminperiod(self.params.period)
        self.time_ma = bt.ind.EMA(period=self.params.period)

    def next(self):
        volume_price_sum = 0
        volume_sum = sum(self.data.volume.get(size=self.params.period))
        for i,(v,p) in enumerate(zip(self.data.volume.get(size=self.params.period),self.data.close.get(size=self.params.period))):
            volume_price_sum += v * p
        if volume_sum == 0:
            volume_sum = 1
        average_price = volume_price_sum / volume_sum
        #print(average_price)
        self.lines.evwap[0] = average_price
        #print(volume_sum)