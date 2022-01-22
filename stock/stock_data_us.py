#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock_data_us.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import datetime
import pandas as pd
#import logging
#from logger import logger
from utils import add_sma
import dtshare as dt
from multiprocessing import Pool

#logger.setLevel(logging.ERROR)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class StockData(object):
    def __init__(self):

        self._symbols = []
        self._symbol_to_name = {}
        self._symbol_to_df = {}

    def get_basic_data(self):
        try:
            basic_datas = dt.stock_us_spot() 
        except:
            pass
        for _, row in basic_datas.iterrows(): 
            symbol = row['symbol']
            name = row['name']
            cname = row['cname']
            self._symbols.append(symbol)
            self._symbol_to_name[symbol] = cname 
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
        #try:
        #    df = dt.stock_us_daily(symbol)
        #    df = add_sma_indicator(df)
        #    #df = df[::-1]
        #    return df
        #except Exception as e:
        #    logger.error('{} download data error: {}'.format(symbol, e))

        #return None

        df = dt.stock_us_daily(symbol)
        df = add_sma(df, 'us')
        return df


if __name__ == '__main__':
    #sd = StockData()
    ##sd.get_basic_data()
    #symbols = sd.get_symbols()
    #print(len(symbols))

    import os
    def mkdir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    mkdir('stockdata/us_train')
    mkdir('stockdata/us_test')
    sd = StockData()

    symbols = sd.get_symbols()

    for symbol in symbols:
        print(symbol)
        try:
            df = sd.get_df_by_symbol(symbol)

            train = df[:'2021-01-01']
            test = df['2021-01-01':]

            if df is not None:
                train.to_csv(os.path.join('stockdata/us_train', symbol + '.csv'))
                test.to_csv(os.path.join('stockdata/us_test', symbol + '.csv'))
        except Exception as e:
            print(e)
