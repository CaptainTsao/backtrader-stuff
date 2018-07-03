import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math

import evwap
import indicators

class WeekylHigh52(bt.Strategy):

    def __init__(self):

        self.orders = dict()
        self.indicators = dict()
        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()
            self.add_indicator(d, 'dc20', indicators.DonchianChannel, period=240)

    def stop(self):
        for d in self.datas:
            self.close(data=d)

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime.date()
        t = self.data.datetime.time()
        print('%s %s, %s' % (dt.isoformat(), t, txt))

    def add_indicator(self, data, name, ind, *args, **kwargs):
        self.indicators[data.params.name][name] = ind(data, *args, **kwargs)

    def get_indicator(self, data, name):
        return self.indicators[data.params.name][name]


    def next(self):
        for i, d in enumerate(self.datas):
            security_name = d.params.name

            if self.orders[security_name]:
                continue

            contracts = int(self.broker.getvalue() / len(self.datas) / d.close[0] * .95)
            # atr = self.get_indicator(d,'atr')

            if self.get_indicator(d, 'dc20').buysig[0]:
                # if self.get_indicator(d,'rsi')[0]  > 50:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                self.orders[security_name] = self.buy_bracket(data=d, size=contracts, exectype=bt.Order.Market,
                                                              stopprice=d.close[0] * .80, limitprice=d.close[0] * 2)

            elif self.get_indicator(d, 'dc20').sellsig[0]:
                # elif self.get_indicator(d,'rsi')[0] < 50:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                #self.orders[security_name] = self.sell_bracket(data=d, size=contracts, exectype=bt.Order.Market,
                #                                               stopprice=d.close[0] * 1.1, limitprice=d.close[0] * .9)

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

        for k, v in self.orders.items():
            if v is None:
                continue
            if isinstance(v, list):
                for o in v:
                    if o.status not in [o.Canceled, o.Margin, o.Rejected, o.Completed, ]:
                        break
                else:
                    self.orders[k] = None
            elif v.status in [v.Canceled, v.Margin, v.Rejected, v.Completed, ]:
                self.orders[k] = None


class Donchian(bt.Strategy):

    def __init__(self):

        self.orders = dict()
        self.indicators = dict()
        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()
            self.add_indicator(d,'dc20',indicators.DonchianChannel,period=360)
            #self.add_indicator(d,'dc10',indicators.DonchianChannel,period=3)
            #self.add_indicator(d,'atr',bt.ind.ATR,period=12)
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

    def do_sizing_simple(self,security_name,data):
        if security_name == 'EURUSD':
            return self.broker.getvalue() *.1
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        # atr = self.strategy.atr[0]
        max_contracts = int((self.broker.getvalue() / margin / len(self.datas))**(1.0 / 1.5))
        #max_contracts = 1
        if max_contracts == 0:
            max_contracts = 1
        return max_contracts


    def next(self):
        if not (datetime.time(15,45) <= self.data.datetime.time() <= datetime.time(16, 00)):
            return
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            if self.orders[security_name]:
                continue

            contracts = self.do_sizing_simple(security_name,d)
            #atr = self.get_indicator(d,'atr')

            if self.get_indicator(d, 'dc20').buysig[0]:
            #if self.get_indicator(d,'rsi')[0]  > 50:
                if self.getposition(d).size > 0:
                    continue
                elif self.getposition(d).size < 0:
                    self.close(data=d)
                self.orders[security_name] = self.buy_bracket(data=d, size=contracts, exectype=bt.Order.Market,stopprice=d.close[0] *.99, limitprice=d.close[0] *1.01)

            elif self.get_indicator(d, 'dc20').sellsig[0]:
            #elif self.get_indicator(d,'rsi')[0] < 50:
                if self.getposition(d).size < 0:
                    continue
                elif self.getposition(d).size > 0:
                    self.close(data=d)
                self.orders[security_name] = self.sell_bracket(data=d,size=contracts, exectype=bt.Order.Market,stopprice=d.close[0] *1.01,limitprice=d.close[0] *.99)


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


class maCross(bt.Strategy):

    def do_sizing_simple(self,security_name,data):
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult
        # atr = self.strategy.atr[0]
        max_contracts = int(self.broker.getvalue() / margin / len(self.datas) / 10)
        return max_contracts

    def do_sizing(self, security_name, data):
        comminfo = self.broker.comminfo[security_name]
        margin = comminfo.margin
        mult = comminfo.params.mult

        pos = self.getposition(data).size

        #strength = self.get_indicator(data, 'strength')[0]
        strength = self.ewmac[0]
        max_contracts = int(self.broker.getvalue() / margin / len(self.datas) / 15)
        max_contracts = max(max_contracts, abs(pos))
        new_pos_size = int(strength * max_contracts)

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
        #self.carry = indicators.CarryStrength(plot=True,subplot=True)
        self.ewmac = indicators.EWMAC()
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
        if not self.data.datetime.time().hour == 15:
          return
        #strengths = []
        #for d in self.datas:
        #    strengths.append((self.get_indicator(d,'strength')[0],d))
        #strengths.sort(key=lambda x: abs(x[0]))
        for i,d in enumerate(self.datas):
            security_name = d.params.name

            contracts = self.do_sizing(security_name,d)

            if abs(self.get_indicator(d,'strength')[0]) < .3:
                if self.getposition(d).size != 0:
                    self.close(data=d)
            elif contracts < 0:
                self.buy(data=d,size=abs(contracts))
            else:
                self.sell(data=d,size=abs(contracts))


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
