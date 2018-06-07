import pandas as pd
import quandl
import os

EXISTING_FILES = os.listdir('quandl_data')
print(EXISTING_FILES)
print(len(EXISTING_FILES))

quandl.ApiConfig.api_key = ''
with open('quandl_data/CHRIS-datasets-codes.csv','r') as f:
    for line in f:
        line = line.strip().split(',')[0]
        out_file = 'quandl_data/' + line.replace('CHRIS/', '') + '.csv'

        if os.path.split(out_file)[1] in EXISTING_FILES:
            continue
        print("fetching",out_file)
        ret = quandl.get(line)


        ret.to_csv(out_file)