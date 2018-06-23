import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import tarfile
import io

ALL_DATAS = [
    #"ES.txt"
      #'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/ES.txt',
      #'C:/Users/mcdof/Documents/kibot_data/forex/60min/EURUSD.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/GC.txt',
      # 'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PA.txt',
      # 'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PL.txt',
      # 'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SI.txt',
      # 'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HG.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NN.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NQ.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NG.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CL.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HO.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/RB.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/TY.txt',
      #'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/EU.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/JY.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/BP.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CD.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/NE.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/AD.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SF.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/DX.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/PX.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/GF.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/LE.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/HE.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/S.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/C.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/BO.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SM.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/W.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/SB.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/KC.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/KW.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/CC.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/OJ.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/RR.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/O.txt',
      #  'C:/Users/mcdof/Documents/kibot_data/cont_futures/60min/LB.txt',
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