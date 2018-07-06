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
