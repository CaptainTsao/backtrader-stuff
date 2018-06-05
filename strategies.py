import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import evwap
import indicators

class maCross(bt.Strategy):

    def do_sizing_simple(self,security_name,data):
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        # atr = self.strategy.atr[0]
        max_contracts = int(self.broker.getvalue() / margin / len(self.datas) / 2)
        return max_contracts

    def do_sizing(self, security_name, data):
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        # atr = self.strategy.atr[0]
        max_contracts = int(self.broker.getvalue() / margin / len(self.datas) / 3)
        # max_contracts = int(self.broker.getcash() / margin / len(self.datas) / 20)
        cash = self.broker.getcash()
        max_contracts_by_cash = int(self.broker.getcash() / margin / len(self.datas) / 20)
        value = self.broker.getvalue()
        pos = self.getposition(data).size
        max_contracts = max(max_contracts, abs(pos))

        prev_strength = self.get_indicator(data, 'strength')[-1]
        if math.isnan(prev_strength):
            prev_strength = 0
        strength = self.get_indicator(data, 'strength')[0]

        new_pos_size = int(strength * max_contracts)
        prev_adjusted_size = int(prev_strength * max_contracts)

        if abs(new_pos_size) > abs(pos):
            pass
            # we need to make sure there's enough cash to increase our position size

        if pos == new_pos_size:
            ret = 0
        elif pos == 0:
            ret = new_pos_size
        elif new_pos_size == 0:
            ret = pos * -1
        elif pos >= 0 and new_pos_size >= 0 or pos <= 0 and new_pos_size <= 0:
            ret = abs(pos) - abs(new_pos_size)
            if new_pos_size < pos:
                ret = abs(ret) * -1
            else:
                ret = abs(ret)
        elif (pos >= 0 and new_pos_size <= 0) or (pos <= 0 and new_pos_size >= 0):
            ret = abs(pos) + abs(new_pos_size)
            if new_pos_size < pos:
                ret = abs(ret) * -1
            else:
                ret = abs(ret)

        #we are making our position bigger, so we need to make sure we have enough cash
        #if abs(new_pos_size) > abs(pos):


        return ret

    def add_indicator(self,data,name,ind,*args,**kwargs):
        self.indicators[data.params.name][name] = ind(data,*args,**kwargs)

    def get_indicator(self,data,name):
        return self.indicators[data.params.name][name]


    def __init__(self):

        self.orders = dict()
        self.indicators = dict()

        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()
            self.add_indicator(d,'strength',indicators.TrendStrength)

    def stop(self):
        for d in self.datas:
            self.close(data=d)


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime.date()
        t  = self.data.datetime.time()
        print('%s %s, %s' % (dt.isoformat(), t, txt))

    def next(self):
        #if not (datetime.time(8, 30) < self.data.datetime.time() < datetime.time(16, 00)):
        #    return
        if datetime.time(0,0) == self.data.datetime.time():
            for d in self.datas:
                pass
                #print(d.params.name,self.getposition(d).size)
        if not (self.data.datetime.time().hour == 15):
            return
        #strengths = []
        #for d in self.datas:
        #    strengths.append((self.get_indicator(d,'strength')[0],d))
        #strengths.sort(key=lambda x: abs(x[0]))
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            contracts = self.do_sizing(security_name,d)

            #if self.get_indicator(d,'strength')[0] < .3:
            #    if self.getposition(d).size != 0:
            #        self.close(data=d)
            if contracts < 0:
                self.sell(data=d,size=abs(contracts))
            else:
                self.buy(data=d,size=abs(contracts))


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
                self.orders[k] = None
                continue
            if v.status in [v.Canceled, v.Margin, v.Rejected, v.Completed, ]:
                self.orders[k] = None
