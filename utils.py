import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os

ALL_DATAS = [
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/GC.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PA.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PL.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SI.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HG.txt',
    #'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/ES.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NN.txt',
    #'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NQ.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NG.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CL.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HO.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/RB.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/TY.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/EU.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/JY.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/BP.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CD.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NE.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/AD.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SF.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/DX.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PX.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/GF.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/LE.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HE.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/S.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/C.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/BO.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SM.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/W.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SB.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/KC.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/KW.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CC.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/OJ.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/RR.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/O.txt',
    'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/LB.txt',
]

def add_data(cerebro):
    for txt in ALL_DATAS:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     tmformat='%H:%M',
                                     name = os.path.splitext(os.path.basename(txt))[0],
                                     timeframe=bt.TimeFrame.Ticks,
                                     fromdate=datetime.datetime(1900, 1, 1),
                                     todate=datetime.datetime(2019, 6, 1),
                                     datetime=0,
                                     time=1,
                                     open=2,
                                     high=3,
                                     low=4,
                                     close=5,
                                     volume=6,
                                     openinterest=-6,
                                     plot=False
                                     )
        cerebro.adddata(data)