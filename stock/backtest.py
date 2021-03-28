#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2021 your company All Rights Reserved
#
# Distributed under terms of the GPLv3 license.
###############################################################

# @file backtest.py
# @author wang
# @date 2021-03-11 22:56
# @brief

import pandas as pd
from stock_strategy import StockStrategy

df = pd.read_csv('raw_data/002647.SZ_仁东控股/20200101.csv')
#df = df.iloc[::-1]
print(df)
ss = StockStrategy()

for i in range(70, len(df)):
    #print('*' * 50)
    #print(df[:i])
    #print(i, df.iloc[i, 1], ss.is_ma30_go_up(df[:i]))
    print(i, df.iloc[-i, 1], ss.is_ma30_go_up(df[-i:]))
#ss.is_ma30_go_up(df)

# set sw=2 ts=2 sts=2 et tw=100
