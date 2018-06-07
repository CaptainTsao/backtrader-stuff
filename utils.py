import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import tarfile
import io

ALL_DATAS = [
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/GC.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/PA.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/PL.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/SI.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/HG.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/ES.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/NN.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/NQ.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/NG.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/CL.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/HO.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/RB.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/TY.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/EU.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/JY.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/BP.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/CD.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/NE.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/AD.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/SF.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/DX.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/PX.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/GF.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/LE.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/HE.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/S.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/C.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/BO.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/SM.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/W.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/SB.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/KC.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/KW.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/CC.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/OJ.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/RR.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/O.txt',
     'C:/Users/mcdof/Documents/kibot_data/cont_futures/daily/LB.txt',
]

def get_quandl_data(symbol,exchange='CME',month='1'):
    csv_name = exchange + '_' + symbol.upper() + str(month) + '.csv'
    with tarfile.open('quandl_data.tar.gz','r') as f:
        member = f.getmember(csv_name)
        ret = f.extractfile(member)
        contents = ret.read().decode("utf-8")

        return btfeed.GenericCSVData(dataname=io.StringIO(contents),
                              dtformat='%m/%d/%Y',
                              name=symbol,
                              timeframe=bt.TimeFrame.Ticks,
                              fromdate=datetime.datetime(1900, 1, 1),
                              todate=datetime.datetime(2019, 6, 1),
                              datetime=0,
                              open=1,
                              high=2,
                              low=3,
                              close=4,
                              volume=7,
                              openinterest=8,
                              plot=False
                              )

get_quandl_data('ES')

def add_data(cerebro):
    for txt in ALL_DATAS:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     #tmformat='%H:%M',
                                     name = os.path.splitext(os.path.basename(txt))[0],
                                     timeframe=bt.TimeFrame.Ticks,
                                     fromdate=datetime.datetime(1900, 1, 1),
                                     todate=datetime.datetime(2019, 6, 1),
                                     datetime=0,
                                     time=-1,
                                     open=1,
                                     high=2,
                                     low=3,
                                     close=4,
                                     volume=5,
                                     openinterest=-6,
                                     plot=False
                                     )
        cerebro.adddata(data)