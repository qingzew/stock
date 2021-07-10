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
from utils import add_sma_indicator
import dtshare as dt

class StockData(object):
    def __init__(self):
        self._symbols = []
        self._symbol_to_name = {}

    def get_basic_data(self):
        basic_datas = dt.stock_hk_spot()
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
            df = dt.stock_hk_daily(symbol)
            df = add_sma_indicator(df)
            df = df[::-1]
            return df
        except Exception as e:
            logger.warning(e)

        return None


if __name__ == '__main__':
    sd = StockData()
    #sd.get_basic_data()
    df = sd.get_df_by_symbol(symbol='00003')
    print(df)
