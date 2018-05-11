import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeed
import datetime
import pandas as pd
from pandas import Series, DataFrame
import random
from copy import deepcopy


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma_fast = bt.indicators.ExponentialMovingAverage(self.datas[0], period=10)
        self.sma_slow = bt.indicators.ExponentialMovingAverage(self.datas[0], period=30)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        #print(self.position)
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Not yet ... we MIGHT BUY if ...
        if self.sma_fast[0] > self.sma_slow[0]:
            if self.position.size <= 0:
                self.close()
                self.order = self.buy()

        elif self.sma_fast[0] < self.sma_slow[0]:
            if self.position.size >= 0:
                self.close()
                #self.order = self.sell()


class PropSizer(bt.Sizer):
    """A position sizer that will buy as many stocks as necessary for a certain proportion of the portfolio
       to be committed to the position, while allowing stocks to be bought in batches (say, 100)"""
    params = {"prop": 0.95, "batch": 100}

    def _getsizing(self, comminfo, cash, data, isbuy):
        """Returns the proper sizing"""

        target = self.broker.getvalue() * self.params.prop  # Ideal total value of the position
        price = data.close[0]
        shares = int(target / price)

        return shares




class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue()  # Get today's account value (cash + stocks)

cerebro = bt.Cerebro(stdstats=False)    # I don't want the default plot objects

cerebro.broker.set_cash(10000)  # Set our starting cash to $1,000,000
cerebro.broker.setcommission(0.00)


data = btfeed.GenericCSVData(dataname="XLK15min.csv",
    dtformat='%m/%d/%Y',
    tmformat='%H%M',

    fromdate=datetime.datetime(2003, 1, 1),
    todate=datetime.datetime(2018 , 12, 28),

    nullvalue=0.0,

    datetime=0,
    time=1,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    timeframe=bt.TimeFrame.Minutes,)

#print(data)
cerebro.adddata(data)    # Give the data to cerebro


cerebro.addobserver(AcctValue)
cerebro.addstrategy(TestStrategy)
cerebro.addsizer(PropSizer)

cerebro.broker.getvalue()
cerebro.run()
cerebro.plot(iplot=True, volume=False)
cerebro.broker.getvalue()