import pandas as pd
import numpy as np

import utils

COLUMNS = ["Date","Open","High","Low","Last","Change","Settle","Volume","Previous Day Open Interest"]

def gen_carry_data(front,later):
    front_csv = pd.read_csv(front)
    later_csv = pd.read_csv(later)
    ret = []
    for front_dp,later_dp in zip(front_csv.iterrows(),later_csv.iterrows()):
        assert front_dp[1].Date == later_dp[1].Date, "Dates {} and {} don't match!".format(front_dp[1].Date, later_dp[1].Date)
        date   = front_dp[1].Date
        open   = front_dp[1].Open - later_dp[1].Open
        high   = front_dp[1].High - later_dp[1].High
        low    = front_dp[1].Low - later_dp[1].Low
        last   = front_dp[1].Last - later_dp[1].Last
        change = front_dp[1].Change - later_dp[1].Change
        volume = front_dp[1].Volume - later_dp[1].Volume
        settle = front_dp[1].Settle - later_dp[1].Settle
        interest = front_dp[1].values[-1] - later_dp[1].values[-1]

        ret.append([date,open,high,low,last,change,settle,volume,interest])

    return pd.DataFrame(ret,columns=COLUMNS)

ret = gen_carry_data("C:/Users/mcdof/Documents/quandl_data/CME_C1.csv","C:/Users/mcdof/Documents/quandl_data/CME_C2.csv")
ret.to_csv("C:/Users/mcdof/Documents/C_carry.csv", float_format='%g',index=False)
print(ret)