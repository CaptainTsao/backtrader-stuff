import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

import observers
import sizers
import strategies
import utils

from commissions import ALL_COMMISSIONS


def main():
    cerebro = bt.Cerebro(stdstats=False)

    for com in ALL_COMMISSIONS:
        cerebro.broker.setcommission(**com)

    cerebro.broker.set_cash(350000) # Set our starting cash to $1,000,000
    cerebro.addobserver(observers.AcctValue)
    utils.add_data(cerebro)
    #cerebro.addstrategy(strategies.maCross)
    cerebro.addstrategy(strategies.Donchian)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.SQN)
    #cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    #cerebro.addobserver(observers.AggregateAssets)
    #cerebro.addobserver(observers.AcctCash)
    #cerebro.addsizer(sizers.mySizer)

    ret = cerebro.run()
    print(ret[0].analyzers.sharperatio.get_analysis())
    print(ret[0].analyzers.sqn.get_analysis())
    cerebro.plot()

if __name__ == '__main__':
    main()