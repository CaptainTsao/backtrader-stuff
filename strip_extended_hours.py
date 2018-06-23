import pandas as pd
import numpy as np


COLUMNS = ["Date","Time","Open","High","Low","Close","Volume"]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def resample_dataframe(df, period):
    ret = []
    for line in df.iterrows():
        hours = int(line[1].Time[0:2])
        if hours >=8 and hours <=16:
            ret.append([line[1].Date,line[1].Time,line[1].Open,line[1].High,line[1].Low,line[1].Close,line[1].Volume])
        #print(hours)


    ret = pd.DataFrame(ret,columns=COLUMNS)
    return ret


df = pd.read_csv('C:/Users/mcdof/Documents/kibot_data/cont_futures/1min/ES.txt',dtype={"Date":np.str,"Time":np.str},engine='c',names=COLUMNS)
resampled = resample_dataframe(df,5)
resampled.to_csv("ES1min.txt", index=False,)