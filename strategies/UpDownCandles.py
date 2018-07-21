import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import indicators

import strategies.BaseStrategy


class UpDownCandles(strategies.BaseStrategy.BaseStrategy):

    def __init__(self):
        super().__init__()
        for d in self.datas:
            self.add_indicator(d,'strength',indicators.UpDownCandleStrength,period=20)
            self.add_indicator(d,'returns',indicators.PercentReturnsPeriod,period=40)

    def next(self):
        #if not (datetime.time(14,00) <= self.data.datetime.time() <= datetime.time(16, 00)):
        #    return
        data_strength_map = dict()
        data_returns_map = dict()
        for i,d in enumerate(self.datas):
            security_name = d.params.name
            if self.orders[security_name]:
                continue

            returns = self.get_indicator(d,'returns')[0]
            #print(returns)
            if  abs(returns) < .01:
                continue
            print(returns)
            contracts = self.do_sizing_simple(security_name,d)
            #returns = returns * .5
            if returns < 0:
                self.orders[security_name] = self.buy_bracket(data=d, size=contracts, exectype=bt.Order.Market,stopprice=d.close[0]*(1 - returns), limitprice=d.close[0]*(1+returns))
            else:
                self.orders[security_name] = self.sell_bracket(data=d,size=contracts, exectype=bt.Order.Market,stopprice=d.close[0]*(1-returns),limitprice=d.close[0]*(1+returns))

            #data_returns_map[d] = returns
            #data_strength_map[d] = self.get_indicator(d,'strength')[0]
            #if returns > 0:



        #returns_sorted = sorted(data_returns_map.items(),key=lambda kv:kv[1])
        strength_sorted = sorted(data_strength_map.items(),key=lambda kv:kv[1])
        #print(returns_sorted)
        #print(strength_sorted)

