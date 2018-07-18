import numpy as np
import pandas as pd
import tempfile

COLUMNS = ["Date","Time","Open","High","Low","Close","Volume"]

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def resample_dataframe(df, period):
    ret = []
    for chunk in chunks(df,period):
        ret.append([chunk.iloc[0]["Date"],
               chunk.iloc[0]["Time"],
               chunk.iloc[0]["Open"],
               max(chunk["High"]),
               min(chunk["Low"]),
               chunk.iloc[-1]["Close"],
               sum(chunk['Volume'])])

    ret = pd.DataFrame(ret,columns=COLUMNS)
    return ret

