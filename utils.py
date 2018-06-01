import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

def add_data(cerebro):
    for txt in ['C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PL.txt',
                'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PA.txt',
                'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/GC.txt',
                'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SI.txt',
                'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HG.txt',

                ]:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     tmformat='%H:%M',
                                     name = os.path.splitext(os.path.basename(txt))[0],
                                     timeframe=bt.TimeFrame.Ticks,
                                     fromdate=datetime.datetime(1990, 1, 1),
                                     todate=datetime.datetime(2019, 6, 1),
                                     datetime=0,
                                     time=1,
                                     open=2,
                                     high=3,
                                     low=4,
                                     close=5,
                                     volume=6,
                                     openinterest=-6)
        cerebro.adddata(data)