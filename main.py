import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

import observers
import sizers
import utils
import strategies.Donchian
import strategies.MACross
import strategies.Turtle
import strategies.BBands

from commissions import ALL_COMMISSIONS
import commissions

GLOBAL_CONFIG = 'FUTURES'

def main():
    cerebro = bt.Cerebro(stdstats=False)

    if GLOBAL_CONFIG == 'FOREX':
        cerebro.broker.setcommission(leverage=50,stocklike=False,commtype=bt.CommInfoBase.COMM_PERC,commission=.0001)
        # Add the new commission scheme
        #comminfo = commissions.forexSpreadCommisionScheme(spread=1.0)
        #cerebro.broker.addcommissioninfo(comminfo)
    elif GLOBAL_CONFIG == 'FUTURES':
        for com in ALL_COMMISSIONS:
            cerebro.broker.setcommission(**com)

    cerebro.broker.set_cash(250000) # Set our starting cash to $1,000,000
    cerebro.addobserver(observers.AcctValue)
    utils.add_data(cerebro)
    #cerebro.addstrategy(strategies.maCross)
    cerebro.addstrategy(strategies.MACross.MACross)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.SQN)
    #cerebro.addanalyzer(bt.analyzers.Returns)
    #cerebro.addanalyzer(bt.analyzers.AnnualReturn)
    #cerebro.addobserver(observers.AggregateAssets)
    #cerebro.addobserver(observers.AcctCash)
    #cerebro.addsizer(sizers.mySizer)

    ret = cerebro.run()
    print(ret[0].analyzers.sharperatio.get_analysis())
    print(ret[0].analyzers.sqn.get_analysis())
    strat = ret[0]
    cerebro.plot()

if __name__ == '__main__':
    main()