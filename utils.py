import datetime
import backtrader as bt
import backtrader.feeds as btfeed
import os
import tarfile
import io
import sys

if sys.platform.startswith('win'):
    BASE_PATH = 'C:/Users/mcdof/Documents/'
else:
    BASE_PATH = '/media/forrest/769A17459A170173/Users/mcdof/Documents/'

DAILIES_FUTURES = [
    BASE_PATH + 'kibot_data/cont_futures/daily/CL.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/HG.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/GC.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/SI.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/ES.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/PA.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/PL.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/GF.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/LE.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/HE.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/S.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/C.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/W.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/O.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/LB.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/OJ.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/CC.txt',
    BASE_PATH + 'kibot_data/cont_futures/daily/KC.txt',

]

DAILIES = [
BASE_PATH + 'kibot_data/stocks/daily/HPQ.txt',
BASE_PATH + 'kibot_data/stocks/daily/GE.txt',
BASE_PATH + 'kibot_data/stocks/daily/KO.txt',
BASE_PATH + 'kibot_data/stocks/daily/IBM.txt',
BASE_PATH + 'kibot_data/stocks/daily/DIS.txt',
BASE_PATH + 'kibot_data/stocks/daily/BA.txt',
BASE_PATH + 'kibot_data/stocks/daily/CAT.txt',
BASE_PATH + 'kibot_data/stocks/daily/ARNC.txt',
BASE_PATH + 'kibot_data/stocks/daily/AA.txt',
BASE_PATH + 'kibot_data/stocks/daily/DD.txt',
BASE_PATH + 'kibot_data/stocks/daily/MO.txt',
BASE_PATH + 'kibot_data/stocks/daily/MRO.txt',
BASE_PATH + 'kibot_data/stocks/daily/CNP.txt',
BASE_PATH + 'kibot_data/stocks/daily/MCD.txt',
BASE_PATH + 'kibot_data/stocks/daily/XOM.txt',
BASE_PATH + 'kibot_data/stocks/daily/JNJ.txt',
BASE_PATH + 'kibot_data/stocks/daily/MRK.txt',
BASE_PATH + 'kibot_data/stocks/daily/UTX.txt',
BASE_PATH + 'kibot_data/stocks/daily/FL.txt',
BASE_PATH + 'kibot_data/stocks/daily/CVX.txt',
BASE_PATH + 'kibot_data/stocks/daily/PG.txt',
BASE_PATH + 'kibot_data/stocks/daily/MMM.txt',
BASE_PATH + 'kibot_data/stocks/daily/AEP.txt',
BASE_PATH + 'kibot_data/stocks/daily/ED.txt',
BASE_PATH + 'kibot_data/stocks/daily/HON.txt',
BASE_PATH + 'kibot_data/stocks/daily/IP.txt',
BASE_PATH + 'kibot_data/stocks/daily/F.txt',
BASE_PATH + 'kibot_data/stocks/daily/DTE.txt',
BASE_PATH + 'kibot_data/stocks/daily/GT.txt',
BASE_PATH + 'kibot_data/stocks/daily/PFE.txt',
BASE_PATH + 'kibot_data/stocks/daily/EK.txt',
BASE_PATH + 'kibot_data/stocks/daily/TXN.txt',
BASE_PATH + 'kibot_data/stocks/daily/BMY.txt',
BASE_PATH + 'kibot_data/stocks/daily/WFC.txt',
BASE_PATH + 'kibot_data/stocks/daily/PBI.txt',
BASE_PATH + 'kibot_data/stocks/daily/HAL.txt',
BASE_PATH + 'kibot_data/stocks/daily/DE.txt',
BASE_PATH + 'kibot_data/stocks/daily/AVP.txt',
BASE_PATH + 'kibot_data/stocks/daily/EMR.txt',
BASE_PATH + 'kibot_data/stocks/daily/ETN.txt',
BASE_PATH + 'kibot_data/stocks/daily/PCG.txt',
BASE_PATH + 'kibot_data/stocks/daily/PEP.txt',
BASE_PATH + 'kibot_data/stocks/daily/WY.txt',
# BASE_PATH + 'kibot_data/stocks/daily/ETR.txt',
# BASE_PATH + 'kibot_data/stocks/daily/LLY.txt',
# BASE_PATH + 'kibot_data/stocks/daily/USB.txt',
# BASE_PATH + 'kibot_data/stocks/daily/WMT.txt',
# BASE_PATH + 'kibot_data/stocks/daily/AXP.txt',
# BASE_PATH + 'kibot_data/stocks/daily/DWDP.txt',
# BASE_PATH + 'kibot_data/stocks/daily/DOW.txt',
# BASE_PATH + 'kibot_data/stocks/daily/PNR.txt',
# BASE_PATH + 'kibot_data/stocks/daily/MATX.txt',
# BASE_PATH + 'kibot_data/stocks/daily/APOG.txt',
# BASE_PATH + 'kibot_data/stocks/daily/NAV.txt',
# BASE_PATH + 'kibot_data/stocks/daily/AVT.txt',
# BASE_PATH + 'kibot_data/stocks/daily/NYT.txt',
# BASE_PATH + 'kibot_data/stocks/daily/CHE.txt',
# BASE_PATH + 'kibot_data/stocks/daily/ALE.txt',
# BASE_PATH + 'kibot_data/stocks/daily/GFF.txt',
# BASE_PATH + 'kibot_data/stocks/daily/SYY.txt',
# BASE_PATH + 'kibot_data/stocks/daily/FRT.txt',
# BASE_PATH + 'kibot_data/stocks/daily/EDE.txt',
# BASE_PATH + 'kibot_data/stocks/daily/UIS.txt',
# BASE_PATH + 'kibot_data/stocks/daily/PHI.txt',
# BASE_PATH + 'kibot_data/stocks/daily/KR.txt',
# BASE_PATH + 'kibot_data/stocks/daily/CL.txt',
# BASE_PATH + 'kibot_data/stocks/daily/AET.txt',
# BASE_PATH + 'kibot_data/stocks/daily/GD.txt',
# BASE_PATH + 'kibot_data/stocks/daily/GAS.txt',
# BASE_PATH + 'kibot_data/stocks/daily/LMT.txt',
# BASE_PATH + 'kibot_data/stocks/daily/PEI.txt',
# BASE_PATH + 'kibot_data/stocks/daily/BP.txt',
# BASE_PATH + 'kibot_data/stocks/daily/SOGC.txt',

]

FOREX_PAIRS = [
    BASE_PATH + 'kibot_data/forex/15min/EURUSD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURJPY.txt',
    #BASE_PATH + 'kibot_data/forex/15min/GBPJPY.txt',
    #BASE_PATH + 'kibot_data/forex/15min/USDJPY.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURAUD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/GBPUSD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURCAD.txt',

    #BASE_PATH + 'kibot_data/forex/15min/AUDUSD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/NZDUSD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/GBPCHF.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURGBP.txt',
    #BASE_PATH + 'kibot_data/forex/15min/AUDCAD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/AUDCHF.txt',
    #BASE_PATH + 'kibot_data/forex/15min/USDCHF.txt',
    #BASE_PATH + 'kibot_data/forex/15min/AUDNZD.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURCHF.txt',
    #BASE_PATH + 'kibot_data/forex/15min/EURNZD.txt',

]

ALL_DATAS = [

    # "/home/forrest/dev/ES.txt"
    #BASE_PATH + 'kibot_data/forex/15min/EURUSD.txt',
    # BASE_PATH + 'kibot_data/cont_futures/15min/GC.txt',
    # BASE_PATH + 'kibot_data/cont_futures/15min/PA.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/PL.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/SI.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/HG.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/NN.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/NQ.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/NG.txt',
    #  BASE_PATH + 'kibot_data/cont_futures/15min/CL.txt',
    #  #  # BASE_PATH + 'kibot_data/cont_futures/15min/HO.txt',
    #  # # # BASE_PATH + 'kibot_data/cont_futures/15min/RB.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/TY.txt',
       BASE_PATH + 'kibot_data/cont_futures/15min/EU.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/JY.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/BP.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/CD.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/NE.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/AD.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/SF.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/DX.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/PX.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/GF.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/LE.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/HE.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/S.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/C.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/BO.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/SM.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/W.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/SB.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/KC.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/KW.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/CC.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/OJ.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/RR.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/O.txt',
    #   BASE_PATH + 'kibot_data/cont_futures/15min/LB.txt',
]

class MyChartData(bt.feed.DataBase):
    def __init__(self):
        super(MyChartData, self).__init__()
        self.buffered_lines = []
        self.f = None


    def start(self):
        # the feed must start ... get the file open (or see if it was open)
        self.f = None
        if hasattr(self.p.dataname, 'read'):
            # A file has been passed in (ex: from a GUI)
            self.f = self.p.dataname
        else:
            # Let an exception propagate
            self.f = open(self.p.dataname, 'r')

    def stop(self):
        if self.f is not None:
            self.f.close()
            self.f = None

    def _load(self):
        if self.f is None:
            return False

        if len(self.buffered_lines) == 0:
            self.buffered_lines = self.f.readlines(10000)

        if not self.buffered_lines:
            return False

        vals = [x.strip() for x in self.buffered_lines.pop(0).split(',')]
        dt = vals[0] + ' ' + vals[1]
        dt = datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M')

        self.lines.datetime[0] = bt.date2num(dt)


        self.lines.open[0] = float(vals[2])
        self.lines.high[0] = float(vals[3])
        self.lines.low[0] = float(vals[4])
        self.lines.close[0] = float(vals[5])
        self.lines.volume[0] = int(float(vals[6]))

        # Say success
        return True

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
                                     fromdate=datetime.datetime(1900, 1, 1),
                                     todate=datetime.datetime(2019, 12, 1),
                                     datetime=0,
                                     time=1,
                                     open=2,
                                     high=3,
                                     low=4,
                                     close=5,
                                     volume=6,
                                     openinterest=-6,
                                     plot=False,
                                     preload=True,
                                     runonce=True
                                     )

        #data = MyChartData(dataname=txt,name=os.path.splitext(os.path.basename(txt))[0])
        cerebro.adddata(data)