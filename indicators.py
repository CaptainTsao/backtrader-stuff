import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import math
import utils
import commissions
import math

class PercentReturnsPeriod(bt.Indicator):
    lines = ('returns',)
    params = (('period',20),)

    def __init__(self):
        self.addminperiod(self.params.period + 2)

    def next(self):
        o = self.data.open[-self.params.period]
        c = self.data.close[0]
        returns = (c - o) / o
        self.lines.returns[0] = returns


class UpDownCandleStrength(bt.Indicator):
    lines = ('strength',)
    params = (('period',20),)

    def __init__(self):
        self.addminperiod(self.params.period + 2)

    def next(self):
        green_candles = 0
        for i in range(0,-self.params.period,-1):
            o = self.data.open[i]
            c =self.data.close[i]
            if c > o:
                green_candles += 1
        self.lines.strength[0] = green_candles / self.params.period

class hilo(bt.ind.PeriodN):
    lines = ('maxi', 'mini',)
    params = (('period', 20),)

    def __init__(self):
        self.lines.maxi = bt.ind.Highest(self.data.high, period=self.p.period)
        self.lines.mini = bt.ind.Lowest(self.data.low, period=self.p.period)

class DonchianChannel(bt.Indicator):
    lines = ('buysig','sellsig')
    params = (('period',20),)

    def __init__(self):
        self.channel = hilo(period=self.params.period)

    def next(self):
        self.lines.buysig[0] = self.data.close[0] >  self.channel.maxi[-1]
        self.lines.sellsig[0] = self.data.close[0] <  self.channel.mini[-1]

class EWMAC(bt.Indicator):
    lines = ('ewmac',)
    params = (('fast_ma',4),('slow_ma',16))

    plotinfo = dict(plot=True,subplot=True)
    plotlines = dict(
        ewmac=dict(ls='--'),
    )

    def __init__(self):
        self.addminperiod(self.params.slow_ma)
        self.ema_fast = bt.ind.EMA(period=self.params.fast_ma)
        self.ema_slow = bt.ind.EMA(period=self.params.slow_ma)
        self.percent_returns = PercentReturns()
        self.stddev_percent_returns = bt.ind.StdDev(self.percent_returns,period=25)

    def next(self):
        print('fast',self.ema_fast[0])
        print('slow',self.ema_slow[0])
        print(' returns',self.percent_returns[0])
        print('stddev returns',self.stddev_percent_returns[0])
        if self.percent_returns[0] == 0.0:
            self.lines.ewmac[0] = 0
        elif self.stddev_percent_returns[0] == 0.0:
            self.lines.ewmac[0] = 0.0
        self.lines.ewmac[0] = (self.ema_fast[0] - self.ema_slow[0]) / (self.stddev_percent_returns[0] * self.datas[0])

class RawReturns(bt.Indicator):
    lines = ('returns',)

    def __init__(self):
        self.addminperiod(2)

    def next(self):
        self.lines.returns[0] = self.data[0] - self.data[-1]


class PercentReturns(bt.Indicator):
    lines = ('returns',)

    def __init__(self):
        self.addminperiod(2)

    def next(self):
        self.lines.returns[0] = self.data[0] / self.data[-1] #- 1.0

class AnnualReturns(bt.Indicator):
    lines = ('annualreturn',)

    def __init__(self):
        pass

    def next(self):
        symbol = self.datas[0].params.name
        month = self.datas[0].datetime.date().month
        distance = commissions.get_next_contract_distance(symbol, month)

        self.lines.annualreturn[0] = self.datas[0] / distance
        if math.isnan(self.lines.annualreturn[0]):
            pass


class CarryStrength(bt.Indicator):

    lines = ('carry',)
    params =(('period',25),)

    plotinfo = dict(subplot=True)
    plotlines = dict(
        carry=dict(ls='--'),
    )

    def __init__(self):
        self.ar = AnnualReturns()
        self.stddef = bt.ind.StdDev(self.ar)

    def next(self):
        self.l.carry[0] = (self.ar[0] / (self.stddef[0] * 16))
        print(self.l.carry[0])


class TrendStrength(bt.Indicator):

    lines = ('strength',)
    params = (('periods',[8,24,48,72,96]),)

    plotinfo = dict(subplot=True)
    plotlines = dict(
        strength=dict(ls='--'),
    )

    def __init__(self):
        self.ma2 = bt.ind.EMA(period=2)
        self.ma4 = bt.ind.EMA(period=4)
        self.ma8 = bt.ind.EMA(period=8)
        self.ma16 = bt.ind.EMA(period=16)
        self.ma32 = bt.ind.EMA(period=32)
        self.ma64 = bt.ind.EMA(period=64)
        self.ma128 = bt.ind.EMA(period=128)
        self.ma256 = bt.ind.EMA(period=256)

    def next(self):
        strength = 0
        fasts = [self.ma2,self.ma4,self.ma8,self.ma16,self.ma32,self.ma64]
        slows = [self.ma8,self.ma16,self.ma32,self.ma64,self.ma128,self.ma256]

        for fast,slow in zip(fasts,slows):
            if fast[0] > slow[0]:
                strength += 1/ len(fasts)
            else:
                strength -= 1/len(fasts)

        self.lines.strength[0] = strength

class EVWAP(bt.Indicator):

    lines = ('evwap',)
    params = (('period',10),)

    plotinfo = dict(subplot=False)
    plotlines = dict(
        evwap=dict(ls='--'),
    )

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