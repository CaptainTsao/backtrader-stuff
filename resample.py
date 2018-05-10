import numpy as np
import pandas as pd

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def resample_dataframe(df, period):
    pass


df = pd.read_csv("D:/XLK.csv")
for x in chunks(df,5):
    print(x)