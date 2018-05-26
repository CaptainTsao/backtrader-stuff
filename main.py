import datetime
import backtrader as bt
import backtrader.feeds as btfeed

class EVWAP(bt.Indicator):

    lines = ('evwap',)
    params = (('period',10),)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.time_ma = bt.ind.EMA(period=self.params.period)

    def next(self):
        volume_price_sum = 0
        volume_sum = sum(self.data.volume.get(size=self.params.period))
        for i,(v,p) in enumerate(zip(self.data.volume.get(size=self.params.period),self.data.close.get(size=self.params.period))):
            volume_price_sum += v * p
        average_price = volume_price_sum / volume_sum
        #print(average_price)
        self.lines.evwap[0] = (average_price + self.time_ma[0])/2
        #print(volume_sum)

class maCross(bt.Strategy):

    def __init__(self):
        self.fast_ma = EVWAP(period=2)
        self.slow_ma = EVWAP(period=8)

        # Cross of macd.macd and macd.signal
        self.cross = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        self.order = None

    def stop(self):
        for d in self.datas:
            self.close(data=d)


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if self.order:
            return

        lot_dollars = self.broker.getvalue() / len(self.datas)*.9

        for i,d in enumerate(self.datas):
            #print(d.close[0])
            dt, dn = self.datetime.date(), d._name
            pos = self.getposition(d).size
            lot_size = int(lot_dollars / d.close[0])
            #lot_size = 2
            if not pos:  # no market / no orders
                if self.cross[-2] == 1 and self.fast_ma[0] > self.slow_ma:
                    print("buying",lot_size)
                    self.order = self.buy(data=d,size=lot_size)
                elif self.cross[-2] == -1 and self.fast_ma[0] < self.slow_ma:
                    print("selling",lot_size)
                    self.order = self.sell(data=d,size=lot_size)
            else:
                if self.cross[-2] == 1 and self.fast_ma[0] > self.slow_ma:
                    self.close(data=d)
                    self.order = self.buy(data=d,size=lot_size)
                elif self.cross[-2] == -1 and self.fast_ma[0] < self.slow_ma:
                    self.close(data=d)
                    self.order = self.sell(data=d, size=lot_size)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                pass
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                pass
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled]:
            self.log('Order Canceled')
        elif order.status in [order.Margin]:
            self.log('Order Margin')
        elif order.status in [order.Rejected]:
            self.log('Order Rejected')

        # Write down: no pending order
        self.order = None

class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue() # Get today's account value (cash + stocks)

def add_data(cerebro):
    for txt in ['GF.txt']:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     tmformat='%H:%M',

                                     fromdate=datetime.datetime(1990, 1, 1),
                                     todate=datetime.datetime(2019, 6, 1),

                                     #  nullvalue=0.0,

                                     datetime=0,
                                     time=1,
                                     open=2,
                                     high=3,
                                     low=4,
                                     close=5,
                                     volume=6,
                                     openinterest=-6)
        cerebro.adddata(data)

cerebro = bt.Cerebro(stdstats=False)

cerebro.broker.set_cash(1000000) # Set our starting cash to $1,000,000
cerebro.addobserver(AcctValue)
add_data(cerebro)
cerebro.addstrategy(maCross)
cerebro.addobserver(bt.observers.DrawDown)

cerebro.run()
cerebro.plot()