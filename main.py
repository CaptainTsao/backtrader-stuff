import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
from commissions import ALL_COMMISSIONS

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
        if volume_sum == 0:
            volume_sum = 1
        average_price = volume_price_sum / volume_sum
        #print(average_price)
        self.lines.evwap[0] = average_price
        #print(volume_sum)


class maCross(bt.Strategy):

    def __init__(self):
        self.fast_ma = bt.ind.EMA(period=128)
        self.slow_ma = bt.ind.EMA(period=512)

        self.atr = bt.ind.ATR(period=20)

        self.cross = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
        self.orders = dict()
        for d in self.datas:
            self.orders[d.params.name] = None

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
            if self.fast_ma[0] > self.slow_ma[0] and self.fast_ma[0] > self.fast_ma[-1] and self.slow_ma[0] > self.slow_ma[-1]:
                self.close(data=d)
                self.buy(data=d)

                #buy_order = self.buy(data=d,transmit=False)
                #trail_stop = self.sell(data=d,parent=buy_order,trailpercent=.02,exectype=bt.Order.StopTrail)
                #self.orders[security_name] = [buy_order,trail_stop]

                #self.orders[security_name] = self.buy_bracket(data=d,limitprice=d.close[0]*1.01,stopprice=d.close[0]*.99,exectype=bt.Order.Market)
            if self.fast_ma[0] < self.slow_ma[0] and self.fast_ma[0] < self.fast_ma[-1] and self.slow_ma[0] < self.slow_ma[-1]:
                self.close(data=d)
                self.sell(data=d)

                #sell_order = self.sell(data=d,transmit=False)
                #trail_stop = self.buy(data=d,parent=sell_order,trailpercent=.02,exectype=bt.Order.StopTrail)
                #self.orders[security_name] = [sell_order,trail_stop]

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
                self.log('BUY EXECUTED, %.6f' % order.executed.price)
            elif order.issell():
                pass
                self.log('SELL EXECUTED, %.6f' % order.executed.price)

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


class mySizer(bt.Sizer):

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        margin = comminfo.margin
        mult = comminfo.params.mult
        atr = self.strategy.atr[0]
        num_contracts = int(self.broker.getvalue() / margin / 10)
        print("buying" if isbuy else "selling",num_contracts)
        return num_contracts

class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue() # Get today's account value (cash + stocks)

def add_data(cerebro):
    for txt in ['C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/AD.txt']:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     tmformat='%H:%M',
                                     name = os.path.splitext(os.path.basename(txt))[0],
                                     timeframe=bt.TimeFrame.Ticks,

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

for com in ALL_COMMISSIONS:
    cerebro.broker.setcommission(**com)

cerebro.broker.set_cash(1000000) # Set our starting cash to $1,000,000
cerebro.addobserver(AcctValue)
add_data(cerebro)
cerebro.addstrategy(maCross)
cerebro.addobserver(bt.observers.DrawDown)
cerebro.addsizer(mySizer)

cerebro.run()
cerebro.plot()