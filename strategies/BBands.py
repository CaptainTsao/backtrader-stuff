import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import evwap
import indicators
import main

class BBands(bt.Strategy):

    def __init__(self):

        self.orders = dict()
        self.indicators = dict()
        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()
            self.add_indicator(d,'bb',bt.ind.BollingerBands,period=20)

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
        if main.GLOBAL_CONFIG == 'FOREX':
            return self.broker.getvalue() / len(self.datas) *10
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        max_contracts = int((self.broker.getvalue() / margin / len(self.datas))**(1.0 / 2.0))
        if max_contracts == 0:
            max_contracts = 1
        return max_contracts


    def next(self):
        #if not (datetime.time(10,00) <= self.data.datetime.time() <= datetime.time(16, 00)):
        #    return
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            contracts = self.do_sizing_simple(security_name,d)

            bb = self.get_indicator(d,'bb')

            if self.getposition(d).size > 0 and d.close[0] < bb.mid[0]:
                self.close(data=d)
            elif self.getposition(d).size < 0 and d.close[0] > bb.mid[0]:
                self.close(data=d)

            if bb.top[0] < d.close[0]:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                self.buy(data=d,size=contracts)

            elif bb.bot[0] > d.close[0]:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                self.sell(data=d,size=contracts)

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