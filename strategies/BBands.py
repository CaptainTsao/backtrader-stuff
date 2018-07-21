import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import indicators

import strategies.BaseStrategy

class BBands(strategies.BaseStrategy.BaseStrategy):

    def __init__(self):
        super().__init__()
        for d in self.datas:
            self.add_indicator(d,'bb',bt.ind.BollingerBands,period=10)

    def next(self):
        #if not (datetime.time(10,00) <= self.data.datetime.time() <= datetime.time(16, 00)):
        #    return
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            contracts = self.do_sizing_simple(security_name,d)

            bb = self.get_indicator(d,'bb')

            if self.getposition(d).size > 0 and d.close[0] > bb.mid[0]:
                self.close(data=d)
            elif self.getposition(d).size < 0 and d.close[0] < bb.mid[0]:
                self.close(data=d)

            if bb.top[0] < d.close[0]:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                self.sell(data=d,size=contracts)

            elif bb.bot[0] > d.close[0]:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                self.buy(data=d,size=contracts)
