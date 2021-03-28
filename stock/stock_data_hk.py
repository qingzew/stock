#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock_data_hk.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import datetime
import tushare as ts 
import pandas as pd
from logger import logger
import akshare as ak

class StockData(object):
    def __init__(self):
        self._symbols = []
        self._symbol_to_name = {}

    def get_basic_data(self):
        basic_datas = ak.stock_hk_spot()
        for _, row in basic_datas.iterrows(): 
            symbol = row['symbol']
            name = row['name']
            self._symbols.append(symbol)
            self._symbol_to_name[symbol] = name 
        return self._symbols,  self._symbol_to_name

    def get_symbols(self):
        if len(self._symbols) == 0:
            self.get_basic_data()
        return self._symbols

    def get_symbol_to_name(self):
        if len(self._symbol_to_name) == 0:
            self.get_basic_data()

        return self._symbol_to_name

    def get_df_by_symbol(self, symbol): 
        try:
            df = ak.stock_hk_daily(symbol)
            df = self._add_sma_indicator(df)
            df = df[::-1]
            return df
        except Exception as e:
            logger.warning(e)

        return None

    def _add_sma_indicator(self, df):
        #df['ma5'] = df['close'].ewm(span=5, adjust=False).mean() 
        #df['ma10'] = df['close'].ewm(span=10, adjust=False).mean() 
        #df['ma20'] = df['close'].ewm(span=20, adjust=False).mean() 
        #df['ma30'] = df['close'].ewm(span=30, adjust=False).mean() 
        #df['ma60'] = df['close'].ewm(span=60, adjust=False).mean() 
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma30'] = df['close'].rolling(window=30).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()
        df = df.fillna(0)
        return df


if __name__ == '__main__':
    sd = StockData()
    sd.get_basic_data()
    df = sd.get_df_by_symbol(symbol='00003')
    print(df)
