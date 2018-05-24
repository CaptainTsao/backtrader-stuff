import datetime
import backtrader as bt
import backtrader.feeds as btfeed


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def stop(self):
        self.close()

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.prev_target= 0
        self.ma_pairs = []

        self.moving_averages = []

        for length in range(10,101,10):
            self.moving_averages.append(bt.ind.EMA(period=length))


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
        target = 0.0
        index = 0
        num_above = 0
        max_num_above = sum(range(0,len(self.moving_averages)))
        for ma in self.moving_averages:
            for test_ma in self.moving_averages[index+1:]:
                if ma[0] > test_ma[0]:
                    num_above += 1
            index += 1

        #print("num above",num_above)
        #print("max num above",max_num_above)

        target = ((num_above/max_num_above) - .5) * 2.0
        #print(target)

        if target < 0:
            target = 0

        if target != self.prev_target:
            self.order_target_percent(target=target*.9)
        self.prev_target = target



class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue() # Get today's account value (cash + stocks)

cerebro = bt.Cerebro(cheat_on_open=True)


data = btfeed.GenericCSVData(dataname="AAPL.txt",
    dtformat='%m/%d/%Y',
    tmformat='%H:%M',

    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2019, 1, 1),

  #  nullvalue=0.0,

    datetime=0,
    time=1,
    open=2,
    high=3,
    low=4,
    close=5,
    volume=6,
    openinterest=-6)

cerebro.broker.set_cash(1000000) # Set our starting cash to $1,000,000
cerebro.addobserver(AcctValue)
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
cerebro.addobserver(bt.observers.DrawDown)

cerebro.run()
cerebro.plot()