import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import time
import observers
import utils
import strategies.Donchian
import strategies.MACross
import strategies.Turtle
import strategies.BBands
import strategies.SimpleMA
import strategies.UpDownCandles

from commissions import ALL_COMMISSIONS
import commissions
import global_config


def main():
    start = time.time()
    cerebro = bt.Cerebro(stdstats=False)

    if global_config.GLOBAL_CONFIG == 'FOREX':
        cerebro.broker.setcommission(leverage=50,stocklike=False,commtype=bt.CommInfoBase.COMM_PERC,commission=.0001)
        # Add the new commission scheme
        #comminfo = commissions.forexSpreadCommisionScheme(spread=1.0)
        #cerebro.broker.addcommissioninfo(comminfo)
    elif global_config.GLOBAL_CONFIG == 'FUTURES':
        for com in ALL_COMMISSIONS:
            cerebro.broker.setcommission(**com)
    elif global_config.GLOBAL_CONFIG == 'STOCK':
        cerebro.broker.setcommission(leverage=1,stocklike=True,commission=.00005,mult=1,margin=None)

    cerebro.broker.set_cash(250000)
    cerebro.addobserver(observers.AcctValue)
    utils.add_data(cerebro)
    cerebro.addstrategy(strategies.Donchian.Donchian)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.SQN)

    ret = cerebro.run()
    print(ret[0].analyzers.sharperatio.get_analysis())
    print(ret[0].analyzers.sqn.get_analysis())
    strat = ret[0]
    end = time.time()
    print("simulation took",end-start,"seconds")
    cerebro.plot()


if __name__ == '__main__':

    main()