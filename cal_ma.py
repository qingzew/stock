import os
import talib
import numpy as np
import pandas as pd

for d in os.listdir('data/ori'):
    files = os.listdir('data/ori/' + d)
    files.sort()

    # close field index
    idx = 5 
    daily_datas = []
    dfs = []
    for f in files:	 
        df = pd.read_csv('data/ori/' + d + '/' + f)
        df = df.iloc[::-1]
        dfs.append(df)
    
    dfs = pd.concat(dfs) 
    dfs = dfs.iloc[:, :11]
    ma5 = talib.MA(dfs.loc[:, 'close'],  timeperiod=5)
    dfs['ma5'] = ma5
    ma10 = talib.MA(dfs.loc[:, 'close'],  timeperiod=10)
    dfs['ma10'] = ma10
    ma20 = talib.MA(dfs.loc[:, 'close'],  timeperiod=20)
    dfs['ma20'] = ma20
    ma40 = talib.MA(dfs.loc[:, 'close'],  timeperiod=40)
    dfs['ma40'] = ma40
    ma99 = talib.MA(dfs.loc[:, 'close'],  timeperiod=99)
    dfs['ma99'] = ma99
    ma250 = talib.MA(dfs.loc[:, 'close'],  timeperiod=250)
    dfs['ma250'] = ma250

    this_save_name = d + '.csv'
    print os.path.join('data/processed/', this_save_name)
    dfs.to_csv(os.path.join('data/processed', this_save_name), index=False, float_format = '%.2f')
