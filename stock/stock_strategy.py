#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock_strategy.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import datetime
from collections import OrderedDict, defaultdict
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

from stock_data import StockData
from logger import logger

class StockStrategy(object):
    """
    stock strategy
    """

    def __init__(self):
        """
        """

    # pricing out of market
    def is_pricing_out_of_market(self, st_data):
        """
        args:
            st_data: stock price data in 10 consecutive days        

        return:
            whether the stock is pricing out of market
        """
        ts_code = st_data.iloc[0, 0]
        # today
        trade_date_0 = st_data.iloc[0, 1]
        open_price_0 = st_data.iloc[0, 2]
        high_price_0 = st_data.iloc[0, 3]
        low_price_0 = st_data.iloc[0, 4]
        close_price_0 = st_data.iloc[0, 5]
        pre_close_0 = st_data.iloc[0, 6]
        #change_0 = st_data.iloc[0, 7]
        pct_change_0 = st_data.iloc[0, 8]
        vol_0 = st_data.iloc[0, 9]

        # yestoday
        trade_date_1 = st_data.iloc[1, 1]
        open_price_1 = st_data.iloc[1, 2]
        high_price_1 = st_data.iloc[1, 3]
        low_price_1 = st_data.iloc[1, 4]
        close_price_1 = st_data.iloc[1, 5]
        pre_close_1 = st_data.iloc[1, 6]
        #change_1 = st_data.iloc[1, 7]
        pct_change_1 = st_data.iloc[1, 8]
        vol_1 = st_data.iloc[1, 9]

        # the day before yesterday
        trade_date_2 = st_data.iloc[2, 1]
        open_price_2 = st_data.iloc[2, 2]
        high_price_2 = st_data.iloc[2, 3]
        low_price_2 = st_data.iloc[2, 4]
        close_price_2 = st_data.iloc[2, 5]
        pre_close_2 = st_data.iloc[2, 6]
        #change_2 = st_data.iloc[2, 7]
        pct_change_2 = st_data.iloc[2, 8]
        vol_2 = st_data.iloc[2, 9]

        logger.debug('date: {} open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(trade_date_0,
            open_price_0, high_price_0, low_price_0, close_price_0, pct_change_0, vol_0))

        logger.debug('date: {} open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(trade_date_1,
            open_price_1, high_price_1, low_price_1, close_price_1, pct_change_1, vol_1))

        logger.debug('date: {} open: {} high: {} low: {} close: {} pct: {} vol: {}'.format(trade_date_2,
            open_price_2, high_price_2, low_price_2, close_price_2, pct_change_2, vol_2))

        if pct_change_0 > 9.95 and pct_change_1 > 9.95:
            logger.debug('====maybe this is the one====')

        flag_poom_1st = False
        if pct_change_0 > 9.95 and abs(low_price_0 - close_price_0) < 0.05:
            if abs(low_price_1 - high_price_1) > 0.1:
                flag_poom_1st = True
            else: 
                logger.debug('poom 1st {} {} fail'.format(ts_code, trade_date_1))
        else:
            logger.debug('poom 1st {} {} fail'.format(ts_code, trade_date_0))

        flag_poom_2ed = False
        if pct_change_0 > 9.95 and abs(low_price_0 - close_price_0) < 0.05:
            if pct_change_1 > 9.95 and abs(low_price_1 - close_price_1) < 0.05:
                #if pct_change_2 <= 0.98 and low_price_2 < high_price_2:
                    #if vol_0 < vol_1 and vol_1 < vol2:
                    #    return True
                if abs(low_price_2 - high_price_2) > 0.1:
                    flag_poom_2ed = True
                else: 
                    logger.debug('poom 2ed {} {} fail'.format(ts_code, trade_date_2))
            else:
                logger.debug('poom 2ed {} {} fail'.format(ts_code, trade_date_1))
        else: 
            logger.debug('poom 2ed {} {} fail'.format(ts_code, trade_date_0))

          
        flag_poom_1 = False 
        if pct_change_0 > 9.95:
            flag_poom_1 = True
        
        flag_poom_2 = False 
        if pct_change_0 > 9.95 and pct_change_1 > 9.95: 
            flag_poom_2 = True

        return flag_poom_1st, flag_poom_2ed, flag_poom_1, flag_poom_2

    # ma go up
    def is_ma_go_up(self, st_data):
        days = 7 
        ma5 = st_data.ix[0:days:1, 'ma5'].tolist()
        ma10 = st_data.ix[0:days:1, 'ma10'].tolist()
        ma20 = st_data.ix[0:days:1, 'ma20'].tolist()

        #ma5_subtract_ma10 = (np.array(ma5) - np.array(ma10)) / np.array(ma10)
        #ma10_subtract_ma20 = (np.array(ma10) - np.array(ma20)) / np.array(ma20)
        ma5_subtract_ma10 = np.array(ma5) - np.array(ma10)
        ma10_subtract_ma20 = np.array(ma10) - np.array(ma20)
        logger.debug('ma5 - ma10 {}'.format(ma5_subtract_ma10))
        logger.debug('ma10 - ma20 {}'.format(ma10_subtract_ma20))
       
        ma5_decrease = all(x / y > 1.3 for x, y in zip(ma5_subtract_ma10[0:], ma5_subtract_ma10[1:]))
        ma10_decrease = all(x / y > 1.3 for x, y in zip(ma10_subtract_ma20[0:], ma10_subtract_ma20[1:]))
  
        ma5_subtract_ma10 = ma5_subtract_ma10 > 0
        ma10_subtract_ma20 = ma10_subtract_ma20 > 0

        def is_two_seg(arr):
            idx = np.where(arr == 0)[0]
            if idx.shape[0] == 0:
                return False
            
            return np.sum(arr[idx[0]:]) == 0
        
        ma5_pattern = False
        ma10_pattern = False
        
        if is_two_seg(ma5_subtract_ma10):
            ma5_pattern = True
        if is_two_seg(ma10_subtract_ma20):
            ma5_pattern = True

        return ma5_decrease and ma5_pattern, ma10_decrease and ma10_pattern

    # vol go up
    def is_vol_go_up(self, st_data):
        days = 5 
        vol = st_data.ix[0:days:1, 'vol'].tolist()

        return all(x < y for x, y in zip(vol[0:], vol[1:]))


if __name__ == '__main__':
    import tushare as ts
    pro = ts.pro_api('95f7a4bf060e97230010a4287cf6db5a5e58c4deadef29f31d966978')
    
    start_date = (datetime.date.today() - datetime.timedelta(days=60)).strftime('%Y%m%d')
    end_date = datetime.date.today().strftime('%Y%m%d')
    df = ts.pro_bar(pro_api=pro, 
            ts_code='000001.SZ', 
            asset='E', 
            start_date=start_date,
            end_date=end_date,
            freq='D',
            adj='qfq')
    #        ma=[5, 10, 20])

    print df
    #ss = StockStrategy()
    #print ss.is_pricing_out_of_market(df)
    #print ss.is_ma_go_up(df)
    #print ss.is_vol_go_up(df)
