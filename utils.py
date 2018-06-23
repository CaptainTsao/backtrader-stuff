import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import tarfile
import io

ALL_DATAS = [
    #"ES.txt"
      'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/ES.txt',
      #'C:/Users/mcdof/Documents/kibot_data/forex/15min/EURUSD.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/GC.txt',
        'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/PA.txt',
        'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/PL.txt',
        'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/SI.txt',
        'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/HG.txt',
      # #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/NN.txt',
      #   'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/NQ.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/NG.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/CL.txt',
      # #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/HO.txt',
      # #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/RB.txt',
      #   'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/TY.txt',
       'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/EU.txt',
        'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/JY.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/BP.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/CD.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/NE.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/AD.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/SF.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/DX.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/PX.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/GF.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/LE.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/HE.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/S.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/C.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/BO.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/SM.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/W.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/SB.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/KC.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/KW.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/CC.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/OJ.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/RR.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/O.txt',
         'C:/Users/mcdof/Documents/kibot_data/cont_futures/15min/LB.txt',
]

def get_quandl_data(symbol,exchange='CME',month='1'):
    csv_name = exchange + '_' + symbol.upper() + str(month) + '.csv'
    with tarfile.open('quandl_data.tar.gz','r') as f:
        member = f.getmember(csv_name)
        ret = f.extractfile(member)
        contents = ret.read().decode("utf-8")

        return btfeed.GenericCSVData(dataname=io.StringIO(contents),
                              dtformat='%Y-%m-%d',
                              name=symbol,
                              timeframe=bt.TimeFrame.Ticks,
                              fromdate=datetime.datetime(2009, 1, 1),
                              todate=datetime.datetime(2010, 1, 1),
                              datetime=0,
                              open=1,
                              high=2,
                              low=3,
                              close=4,
                              volume=7,
                              openinterest=8,
                              plot=False
                              )


def add_data(cerebro):
    for txt in ALL_DATAS:
        data = btfeed.GenericCSVData(dataname=txt,
                                     dtformat='%m/%d/%Y',
                                     tmformat='%H:%M',
                                     name = os.path.splitext(os.path.basename(txt))[0],
                                     timeframe=bt.TimeFrame.Ticks,
                                     fromdate=datetime.datetime(2008, 1, 1),
                                     todate=datetime.datetime(2019, 12, 1),
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