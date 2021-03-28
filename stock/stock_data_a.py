#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock_data_a.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import datetime
import tushare as ts 
from logger import logger

class StockData(object):
    def __init__(self):
        self.pro = ts.pro_api('7e0df022a3af325bdf68870f9ca63abd4c8c79d35c1eaef2c3a69a98')
        self._symbols = []
        self._symbol_to_name = {}

    def get_basic_data(self):
        basic_datas = self.pro.stock_basic(exchange_id='', list_status='L', 
                fields='ts_code,symbol,name,area,industry,list_date')
    
        self._symbols = []
        self._symbol_to_name = {}
        for _, row in basic_datas.iterrows():
            symbol = row['ts_code']
            self._symbols.append(symbol)
            self._symbol_to_name[symbol] = row['name']

        return self._symbols, self._symbol_to_name

    def get_symbols(self):
        if len(self._symbols) == 0:
            self.get_basic_data()

        return self._symbols

    def get_symbol_to_name(self):
        if len(self._symbol_to_name) == 0:
            self.get_basic_data()

        return self._symbol_to_name

    def get_df_by_symbol(self, symbol, start_date, end_date,
            ma=[]):
        try:
            df = ts.pro_bar(api=self.pro, 
                    ts_code=symbol,
                    asset='E', 
                    start_date=start_date, 
            	    end_date=end_date, 
            	    freq='D',
            	    adj='qfq',
                    ma=ma)

            return df
        except Exception as e:
            print(e)
            logger.warning(e)


    def get_trade_cal(self):
        #start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y%m%d')
        #end_date = datetime.date.today().strftime('%Y%m%d')
        #trade_cal = self.pro.trade_cal(exchange='', end_date=end_date)
        trade_cal = self.pro.trade_cal()
        return trade_cal[::-1]

if __name__ == '__main__':
    sd = StockData()
    sd.get_basic_data()
    sd.get_trade_cal()
    #df = sd.get_df_by_st_code('000001.SZ', '20190201', '20190309', ma=[5, 10])
    #print df.ix[0:5:2, 'ma5'].tolist()
    #for idx, v1 in df.ix[0:5:2, 'ma5'].iteritems():
    #    print idx, v1

    #for idx, row in df.ix[0:5:2, ['ma5', 'ma_v_5']].iterrows():
    #    print idx, row['ma5']


    #print sd.get_trade_cal()


