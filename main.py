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

    cerebro.broker.set_cash(1000000) # Set our starting cash to $1,000,000
    cerebro.addobserver(observers.AcctValue)
    utils.add_data(cerebro)
    cerebro.addstrategy(strategies.maCross)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addsizer(sizers.mySizer)

    cerebro.run()
    cerebro.plot()

if __name__ == '__main__':
    main()