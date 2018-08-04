import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import indicators


import strategies.BaseStrategy

class Donchian(strategies.BaseStrategy.BaseStrategy):

    def __init__(self):
        super().__init__()
        for d in self.datas:
            self.add_indicator(d,'dc20',indicators.DonchianChannel,period=48)
            #self.add_indicator(d,'atr',bt.ind.ATR,period=24)

    def next(self):
        if not (datetime.time(11,00) <= self.data.datetime.time() <= datetime.time(16, 00)):
            return
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            if self.orders[security_name]:
                continue
            date = self.data.datetime.date()
            contracts = self.do_sizing_simple(security_name,d)
            valid_til = datetime.datetime(year=date.year,month=date.month,day=date.day,hour=23,minute=45)

            if self.get_indicator(d, 'dc20').sellsig[0]:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                #self.buy(data=d,size=contracts)
                o = self.orders[security_name] = self.buy_bracket(data=d, size=contracts, price=d.close[0],stopprice=d.close[0]*.99, limitprice=d.close[0]*1.01,valid=bt.Order.DAY)
                self.record_bracket(o)
            elif self.get_indicator(d, 'dc20').buysig[0]:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                #self.sell(data=d,size=contracts)
                o = self.orders[security_name] = self.sell_bracket(data=d,size=contracts, price=d.close[0],stopprice=d.close[0]*1.01,limitprice=d.close[0]*.99,valid=bt.Order.DAY)
                self.record_bracket(o)