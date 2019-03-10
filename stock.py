#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""
import datetime
from stock_data import StockData
from stock_strategy import StockStrategy
from collections import OrderedDict, defaultdict
import pandas as pd
from pandas import Series, DataFrame

from logger import logger

class Stock(object):
    """
    call StockData and StockStrategy to predict stock
    """

    def __init__(self):
        """
        """
        self._ts_code_to_strategy = defaultdict(lambda: defaultdict(lambda:0))
     
        self._sd = StockData()
        self._ss = StockStrategy()

        self._st_data = defaultdict(DataFrame)

    def init_data(self, ts_codes=None, days=60):
        """
        get stock data for once
        args:
            ts_codes: which stock to get, default is all
            days: how much days to get, default is 30
        return:
            basic datas for specified stock
        """
        start_date = (datetime.date.today() - datetime.timedelta(days=days + 10)).strftime('%Y%m%d')
        end_date = datetime.date.today().strftime('%Y%m%d')

        trade_cal = self._sd.get_trade_cal()
        include_days = []
        for idx, row in trade_cal.iterrows():
            if row['is_open'] == 1:
                include_days.append(row['cal_date'])

            if len(include_days) == days:
                break
        if ts_codes is None:
            ts_codes = self._sd.get_ts_codes()
        elif not isinstance(ts_codes, list):
            ts_codes = [ts_codes,]

        for ts_code in ts_codes:
            try:
                df = self._sd.get_df_by_st_code(ts_code,
                        start_date=include_days[-1],
                        end_date=include_days[0],
                        ma=[5, 10, 20])

                self._st_data[ts_code] = df
            except Exception as e:
                logger.warning(e)

    def get_poom(self):
        """
        args:
        returns:
            whether the stock is pricing out of market
        """
        pricing_out_of_market_1st = []
        pricing_out_of_market_2ed = []
        ts_code_to_name = self._sd.get_ts_code_to_name() 
        for ts_code, df in self._st_data.items():
            try:
                flag_1st, flag_2ed = self._ss.is_pricing_out_of_market(df)
                if flag_1st:
                    pricing_out_of_market_1st.append([ts_code, ts_code_to_name[ts_code]])

                if flag_2ed:
                    pricing_out_of_market_2ed.append([ts_code, ts_code_to_name[ts_code]])
                
                self._ts_code_to_strategy[ts_code]['poom_1st'] = flag_1st
                self._ts_code_to_strategy[ts_code]['poom_2ed'] = flag_2ed

            except Exception as e:
                logger.warning(e)
          
                           
        return pricing_out_of_market_1st, pricing_out_of_market_2ed
  
    def get_ma_go_up(self):
        ma_go_up = []

        ts_code_to_name = self._sd.get_ts_code_to_name() 
        for ts_code, df in self._st_data.items():
            try:
                ma5_flag, ma10_flag = self._ss.is_ma_go_up(df)
                if ma5_flag:
                    ma_go_up.append([ts_code, ts_code_to_name[ts_code]])

                self._ts_code_to_strategy[ts_code]['ma5'] = ma5_flag 
                self._ts_code_to_strategy[ts_code]['ma10'] = ma10_flag 
            except Exception as e:
                logger.warning(e)

        return ma_go_up 

if __name__ == '__main__':
    stock = Stock()
    stock.init_data(['000001.SZ'])
    print stock._st_data['000001.SZ']
    #print stock.get_poom()
    print stock.get_ma_go_up()    
    
