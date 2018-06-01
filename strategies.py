import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os


class maCross(bt.Strategy):

    def add_indicator(self,data,name,ind,**kwargs):
        self.indicators[data.params.name][name] = ind(**kwargs)

    def get_indicator(self,data,name,index):
        return self.indicators[data.params.name][name][index]


    def __init__(self):

        self.orders = dict()
        self.indicators = dict()

        for d in self.datas:
            self.orders[d.params.name] = None
            self.indicators[d.params.name] = dict()

            self.add_indicator(d,'fast_ma',bt.ind.SMA,period=2)
            self.add_indicator(d,'slow_ma',bt.ind.SMA,period=20)

    def stop(self):
        for d in self.datas:
            self.close(data=d)


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime.date()
        t  = self.data.datetime.time()
        print('%s %s, %s' % (dt.isoformat(), t, txt))

    def next(self):
        if not (datetime.time(8, 30) < self.data.datetime.time() < datetime.time(16, 00)):
            return

        for i,d in enumerate(self.datas):
            security_name = d.params.name

            # we only allow one outstanding backet order per security. if this is not none, that means we have
            # a pending buy / stop loss / profit, so we continue
            if self.orders[security_name] is not None:
                continue

            pos = self.getposition(d).size
            #assert(not pos)
            if self.get_indicator(d,'fast_ma',0) > self.get_indicator(d,'slow_ma',0) and \
                    self.get_indicator(d, 'fast_ma', 0) > self.get_indicator(d,'fast_ma',-1) and \
                    self.get_indicator(d, 'slow_ma', 0) > self.get_indicator(d,'slow_ma',-1):
                #self.close(data=d)
                #self.buy(data=d)

                buy_order = self.buy(data=d,transmit=False)
                trail_stop = self.sell(data=d,parent=buy_order,trailpercent=.02,exectype=bt.Order.StopTrail)
                self.orders[security_name] = [buy_order,trail_stop]

                #self.orders[security_name] = self.buy_bracket(data=d,limitprice=d.close[0]*1.01,stopprice=d.close[0]*.99,exectype=bt.Order.Market)
            if self.get_indicator(d,'fast_ma',0) <self.get_indicator(d,'slow_ma',0) and \
                    self.get_indicator(d, 'fast_ma', 0) < self.get_indicator(d,'fast_ma',-1) and \
                    self.get_indicator(d, 'slow_ma', 0) < self.get_indicator(d,'slow_ma',-1):
                #self.close(data=d)
                #self.sell(data=d)

                sell_order = self.sell(data=d,transmit=False)
                trail_stop = self.buy(data=d,parent=sell_order,trailpercent=.02,exectype=bt.Order.StopTrail)
                self.orders[security_name] = [sell_order,trail_stop]

                #self.orders[security_name] = self.buy_bracket(data=d,limitprice=d.close[0]*.99,stopprice=d.close[0]*1.01,exectype=bt.Order.Market)


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
            for o in v:
                if not o.status in [o.Canceled,o.Margin,o.Rejected,o.Completed,]:
                    break
            else:
                self.orders[k] = None
