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
    #def is_ma_go_up(self, st_data):
    #    days = 4 
    #    ma5 = st_data.ix[0:days:1, 'ma5'].tolist()
    #    ma10 = st_data.ix[0:days:1, 'ma10'].tolist()
    #    ma20 = st_data.ix[0:days:1, 'ma20'].tolist()

    #    if ma5[0] <= ma[-1]:
    #        return False, False

    #    #ma5_subtract_ma10 = (np.array(ma5) - np.array(ma10)) / np.array(ma10)
    #    #ma10_subtract_ma20 = (np.array(ma10) - np.array(ma20)) / np.array(ma20)
    #    ma5_subtract_ma10 = np.array(ma5) - np.array(ma10)
    #    ma10_subtract_ma20 = np.array(ma10) - np.array(ma20)
    #    logger.debug('ma5 - ma10 {}'.format(ma5_subtract_ma10))
    #    logger.debug('ma10 - ma20 {}'.format(ma10_subtract_ma20))
    #   
    #    #ma5_decrease = all(x / y > 1.05 for x, y in zip(ma5_subtract_ma10[0:], ma5_subtract_ma10[1:]))
    #    #ma10_decrease = all(x / y > 1.03 for x, y in zip(ma10_subtract_ma20[0:], ma10_subtract_ma20[1:]))
    #    #ma5_subtract_ma10 = ma5_subtract_ma10 > 0
    #    #ma10_subtract_ma20 = ma10_subtract_ma20 > 0

    #    ma5_decrease = all(x / y > 1.0 for x, y in zip(ma5_subtract_ma10[0:], ma5_subtract_ma10[1:]))
    #    ma10_decrease = all(x / y > 1.0 for x, y in zip(ma10_subtract_ma20[0:], ma10_subtract_ma20[1:]))

    #    def is_two_seg(arr):
    #        idx = np.where(arr == 0)[0]
    #        if idx.shape[0] == 0:
    #            return False
    #        
    #        return np.sum(arr[idx[0]:]) == 0
    #    
    #    ma5_pattern = False
    #    ma10_pattern = False
    #    
    #    if is_two_seg(ma5_subtract_ma10):
    #        ma5_pattern = True
    #    if is_two_seg(ma10_subtract_ma20):
    #        ma5_pattern = True

    #    return ma5_decrease and ma5_pattern, ma10_decrease and ma10_pattern

    # ma go up
    def is_ma_go_up(self, st_data):
        ts_code = st_data.iloc[0, 0]

        days = 4 
        tmp_data = st_data[:days]
        ma5 = tmp_data.loc[:, 'ma5'].tolist()
        ma10 = tmp_data.loc[:, 'ma10'].tolist()
        ma20 = tmp_data.loc[:, 'ma20'].tolist()
        ma30 = tmp_data.loc[:, 'ma30'].tolist()
        ma60 = tmp_data.loc[:, 'ma60'].tolist()

        #ma5 = st_data.ix[0:days:1, 'ma5'].tolist()
        #ma10 = st_data.ix[0:days:1, 'ma10'].tolist()
        #ma20 = st_data.ix[0:days:1, 'ma20'].tolist()
        logger.debug('{} ma5: {}'.format(ts_code, ma5))
        logger.debug('{} ma10: {}'.format(ts_code, ma10))
        logger.debug('{} ma20: {}'.format(ts_code, ma20))
        logger.debug('{} ma30: {}'.format(ts_code, ma30))
        logger.debug('{} ma60: {}'.format(ts_code, ma60))

        if ma5[0] <= ma5[-1] or ma10[0] <= ma10[-1] or ma20[0] < ma20[-1]:
            logger.debug('{} ma is going down'.format(ts_code))
            return {} 

        #if ma5[0] / ma5[-1] < 1.1:
        #    logger.debug('ma is going down')
        #    return {} 

        ma5_ratio = np.array([round(x / y, 2) for x, y in zip(ma5[0:], ma10[0:])])
        ma10_ratio = np.array([round(x / y, 2) for x, y in zip(ma10[0:], ma20[0:])])
        ma20_ratio = np.array([round(x / y, 2) for x, y in zip(ma20[0:], ma30[0:])])
        ma30_ratio = np.array([round(x / y, 2) for x, y in zip(ma30[0:], ma60[0:])])

        ma5_sort = ma5_ratio[np.where(ma5_ratio > 1.)[0]]
        ma10_sort = ma10_ratio[np.where(ma10_ratio > 1.)[0]]
        ma20_sort = ma20_ratio[np.where(ma20_ratio > 1.)[0]]
        ma30_sort = ma30_ratio[np.where(ma30_ratio > 1.)[0]]
        is_ma5_sort = all((x > y) for x, y in zip(ma5_sort[0:], ma5_sort[1:])) and len(ma5_sort) > 0
        is_ma10_sort = all((x > y) for x, y in zip(ma10_sort[0:], ma10_sort[1:])) and len(ma10_sort) > 0
        is_ma20_sort = all((x > y)  for x, y in zip(ma20_sort[0:], ma20_sort[1:])) and len(ma20_sort) > 0
        is_ma30_sort = all((x > y) for x, y in zip(ma30_sort[0:], ma30_sort[1:])) and len(ma30_sort) > 0
        logger.debug('{} ma5 sort: {} {}'.format(ts_code, ma5_sort, is_ma5_sort))
        logger.debug('{} ma10 sort: {} {}'.format(ts_code, ma10_sort, is_ma10_sort))
        logger.debug('{} ma20 sort: {} {}'.format(ts_code, ma20_sort, is_ma20_sort))
        logger.debug('{} ma30 sort: {} {}'.format(ts_code, ma30_sort, is_ma30_sort))

        def is_two_seg(arr):
            idx = np.where(arr == 0)[0]
            if idx.shape[0] == 0 or idx.shape[0] > days / 2:
                return False 
            
            return np.sum(arr[idx[0]:]) == 0

        is_ma5_two_seg = False
        is_ma10_two_seg = False
        is_ma20_two_seg = False
        is_ma30_two_seg = False
        ma5_two_seg = np.array([int(e) for e in ma5_ratio > 1.])
        ma10_two_seg = np.array([int(e) for e in ma10_ratio > 1.])
        ma20_two_seg = np.array([int(e) for e in ma20_ratio > 1.])
        ma30_two_seg = np.array([int(e) for e in ma30_ratio > 1.])

        if is_two_seg(ma5_two_seg):
            is_ma5_two_seg = True
        if is_two_seg(ma10_two_seg):
            is_ma10_two_seg = True
        if is_two_seg(ma20_two_seg):
            is_ma20_two_seg = True
        if is_two_seg(ma30_two_seg):
            is_ma30_two_seg = True

        logger.debug('{} ma5 two seg: {} {}'.format(ts_code, ma5_two_seg, is_ma5_two_seg))
        logger.debug('{} ma10 two seg: {} {}'.format(ts_code, ma10_two_seg, is_ma10_two_seg))
        logger.debug('{} ma20 two seg: {} {}'.format(ts_code, ma20_two_seg, is_ma20_two_seg))
        logger.debug('{} ma30 two seg: {} {}'.format(ts_code, ma30_two_seg, is_ma30_two_seg))

        ma_sort_short = is_ma5_sort and is_ma10_sort
        ma_sort_medium = is_ma5_sort and is_ma10_sort and is_ma20_sort
        ma_sort_long = is_ma5_sort and is_ma10_sort and is_ma20_sort and is_ma30_sort

        ma_short = (is_ma5_sort and is_ma5_two_seg) and (is_ma10_sort and is_ma10_two_seg) 
        ma_medium = (is_ma5_sort and is_ma5_two_seg) and (is_ma10_sort and is_ma10_two_seg) \
                and (is_ma20_sort and is_ma20_two_seg)
        ma_long = (is_ma5_sort and is_ma5_two_seg) and (is_ma10_sort and is_ma10_two_seg) \
                and (is_ma20_sort and is_ma20_two_seg) and (is_ma30_sort and is_ma30_two_seg)

        ret = {
            'ma_sort_short': ma_sort_short, 
            'ma_sort_medium': ma_sort_medium, 
            'ma_sort_long': ma_sort_long, 
            'ma_short': ma_short, 
            'ma_medium': ma_medium, 
            'ma_long': ma_long, 
        }
        logger.debug('{} ret: {}'.format(ts_code, ret))

        return ret

    
    def is_ma30_go_up(self, st_data):
        days = 20 
        if len(st_data) < days:
            return False 

        ts_code = st_data.iloc[0, 0]

        tmp_data = st_data[:days]
        #max_min_scaler = lambda x : (x-np.min(x))/(np.max(x)-np.min(x))
        #tmp_data[['ma5']] = tmp_data[['ma5']].apply(max_min_scaler) 
        #tmp_data[['ma10']] = tmp_data[['ma10']].apply(max_min_scaler) 
        #tmp_data[['ma20']] = tmp_data[['ma20']].apply(max_min_scaler) 
        #tmp_data[['ma30']] = tmp_data[['ma30']].apply(max_min_scaler) 
        #tmp_data[['ma60']] = tmp_data[['ma60']].apply(max_min_scaler) 

        ma5 = tmp_data.loc[:, 'ma5'].tolist()
        ma10 = tmp_data.loc[:, 'ma10'].tolist()
        ma20 = tmp_data.loc[:, 'ma20'].tolist()
        ma30 = tmp_data.loc[:, 'ma30'].tolist()
        ma60 = tmp_data.loc[:, 'ma60'].tolist()

        #ma5 = st_data.ix[0:days:1, 'ma5'].tolist()
        #ma10 = st_data.ix[0:days:1, 'ma10'].tolist()
        #ma20 = st_data.ix[0:days:1, 'ma20'].tolist()
        #logger.debug('{} ma5: {}'.format(ts_code, ma5))
        #logger.debug('{} ma10: {}'.format(ts_code, ma10))
        #logger.debug('{} ma20: {}'.format(ts_code, ma20))
        #logger.debug('{} ma30: {}'.format(ts_code, ma30))
        #logger.debug('{} ma60: {}'.format(ts_code, ma60))

        if ma5[0] <= ma5[-1] or ma10[0] <= ma10[-1] or ma20[0] < ma20[-1]:
            logger.debug('{} ma is going down'.format(ts_code))
            return False

        def diff_ratio(data):
            res = []
            for i in range(len(data) - 1):
                res.append((data[i] - data[i + 1]) / (data[i + 1] + 1e-6))
            return np.array(res)
            
        ma5_angle = np.arctan(diff_ratio(ma5) * 100) * 180 / 3.1416
        ma10_angle = np.arctan(diff_ratio(ma10) * 100) * 180 / 3.1416
        ma20_angle = np.arctan(diff_ratio(ma20) * 100) * 180 / 3.1416
        ma30_angle = np.arctan(diff_ratio(ma30) * 100) * 180 / 3.1416
        ma60_angle = np.arctan(diff_ratio(ma60) * 100) * 180 / 3.1416

        #logger.debug('ma5_angle: {}'.format(ma5_angle))
        #logger.debug('ma10_angle: {}'.format(ma10_angle))
        #logger.debug('ma20_angle: {}'.format(ma20_angle))
        #logger.debug('ma30_angle: {}'.format(ma30_angle))
        #logger.debug('ma60_angle: {}'.format(ma60_angle))

        
        def is_true(data):
            for i in range(len(data) - 1):
                if not (data[i] > 10 and data[i] < 55 and \
                        abs(data[i] - data[i + 1]) < 10):
                    return False
            return True

        def is_true2(data1, data2):
            for d1, d2 in zip(data1, data2):
                if d1 < d2:
                    return False
            return True

        logger.debug('{} ma10 angle: {}'.format(ts_code, ma10_angle))
        logger.debug('{} ma20 angle: {}'.format(ts_code, ma20_angle))
        logger.debug('{} ma30 angle: {}'.format(ts_code, ma30_angle))
        logger.debug('{} ma10 tag: {}'.format(ts_code, is_true(ma10_angle)))
        logger.debug('{} ma20 tag: {}'.format(ts_code, is_true(ma20_angle)))
        logger.debug('{} ma30 tag: {}'.format(ts_code, is_true(ma30_angle)))
        #return is_true(ma20_angle) or is_true(ma30_angle)
        return is_true2(ma5, ma10) and is_true(ma30_angle)


    # vol go up
    def is_vol_go_up(self, st_data):
        days = 5 
        vol = st_data.loc[0:days:1, 'vol'].tolist()

        return all(x < y for x, y in zip(vol[0:], vol[1:]))


if __name__ == '__main__':
    pass
