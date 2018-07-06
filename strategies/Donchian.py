import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import evwap
import indicators

class Donchian(bt.Strategy):

    def __init__(self):

        self.orders = dict()
        self.indicators = dict()
        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()
            self.add_indicator(d,'dc20',indicators.DonchianChannel,period=20)
            #self.add_indicator(d,'dc10',indicators.DonchianChannel,period=3)
            #self.add_indicator(d,'atr',bt.ind.ATR,period=360)
            #self.add_indicator(d,'rsi',bt.ind.RSI,period=14)
            #self.add_indicator(d,'fast_ma',bt.ind.SMA,period=24)
            #self.add_indicator(d,'slow_ma',bt.ind.SMA,period=120)

    def stop(self):
        for d in self.datas:
            self.close(data=d)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime.date()
        t  = self.data.datetime.time()
        print('%s %s, %s' % (dt.isoformat(), t, txt))

    def add_indicator(self,data,name,ind,*args,**kwargs):
        self.indicators[data.params.name][name] = ind(data,*args,**kwargs)

    def get_indicator(self,data,name):
        return self.indicators[data.params.name][name]

    def do_sizing_simple(self,security_name, data):
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        max_contracts = int((self.broker.getvalue() / margin / len(self.datas))**(1.0 / 2))
        if max_contracts == 0:
            max_contracts = 1
        return max_contracts


    def next(self):
        #if not (datetime.time(15,00) <= self.data.datetime.time() <= datetime.time(16, 00)):
        #    return
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            if self.orders[security_name]:
                continue

            contracts = self.do_sizing_simple(security_name,d)
            #atr = self.get_indicator(d,'atr')

            if self.get_indicator(d, 'dc20').buysig[0]:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                self.orders[security_name] = self.buy_bracket(data=d, size=contracts, price=d.close[0],stopprice=d.close[0]*.99, limitprice=d.close[0]*1.01,)

            elif self.get_indicator(d, 'dc20').sellsig[0]:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                self.orders[security_name] = self.sell_bracket(data=d,size=contracts, price=d.close[0],stopprice=d.close[0]*1.01,limitprice=d.close[0]*.99)


    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        security_name = order.params.data.params.name
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                self.log('{} BUY EXECUTED, {}'.format(security_name, order.executed.price))
            elif order.issell():
                pass
                self.log('{} SELL EXECUTED, {}'.format(security_name, order.executed.price))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')

        for k,v in self.orders.items():
            if v is None:
                continue
            if isinstance(v,list):
                for o in v:
                    if o.status not in [o.Canceled, o.Margin, o.Rejected, o.Completed, ]:
                        break
                else:
                    self.orders[k] = None
            elif v.status in [v.Canceled, v.Margin, v.Rejected, v.Completed, ]:
                self.orders[k] = None