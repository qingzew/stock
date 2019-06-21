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
import os
import requests
import datetime
from stock_data import StockData
from stock_strategy import StockStrategy
from collections import OrderedDict, defaultdict
import pandas as pd
from pandas import Series, DataFrame

from logger import logger
from collections import OrderedDict

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
        
        #self._mp = OrderedDict([
        #        ('##一字板\n\n', 'poom_1st'),
        #        ('##二字板\n\n', 'poom_2ed'),
        #        #('##首板\n\n', 'poom_1'),
        #        #('##二板\n\n', 'poom_2'),
        #        ('##多头1\n\n', 'ma5'),
        #        ('##多头2\n\n', 'ma10'),
        #        #('##增量\n\n', 'vol')])
        #self._mp = OrderedDict([
        #        ('##一字板\n\n', 'poom_1st'),
        #        ('##二字板\n\n', 'poom_2ed'),
        #        ('##多头0\n\n', 'ma'),
        #        ('##多头1\n\n', 'ma5'),
        #        ('##多头2\n\n', 'ma10')])
        self._mp = OrderedDict([
                ('###一字板\n\n', 'poom_1st'),
                ('###二字板\n\n', 'poom_2ed'),
                ('###ma5&10&20长排列\n\n', 'ma_sort_short'),
                ('###ma5&10&20&30长排列\n\n', 'ma_sort_medium'),
                ('###ma5&10&20&30&60长排列\n\n', 'ma_sort_long'),
                ('###ma5&10&20短排列\n\n', 'ma_short'),
                ('###ma5&10&20&30短排列\n\n', 'ma_medium'),
                ('###ma5&10&20&30&60短排列\n\n', 'ma_long'),
                ])


    def init_data(self, ts_codes=None, days=90):
        """
        get stock data for once
        args:
            ts_codes: which stock to get, default is all
            days: how much days to get, default is 30
        return:
            basic datas for specified stock
        """
        start_date = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y%m%d')
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
                        ma=[5, 10, 20, 30, 60])

                self._st_data[ts_code] = df
            except Exception as e:
                logger.warning(e)

    def get_ts_name_by_code(self, ts_code):
        ts_code_to_name = self._sd.get_ts_code_to_name() 
        return ts_code_to_name[ts_code]
    
    def get_strategy_result(self):
        return self._ts_code_to_strategy

    def get_poom(self):
        """
        args:
        returns:
            whether the stock is pricing out of market
        """
        for ts_code, df in self._st_data.items():
            try:
                flag_poom_1st, flag_poom_2ed, flag_poom_1, flag_poom_2 = \
                        self._ss.is_pricing_out_of_market(df)
                
                self._ts_code_to_strategy[ts_code]['poom_1st'] = flag_poom_1st
                self._ts_code_to_strategy[ts_code]['poom_2ed'] = flag_poom_2ed
                self._ts_code_to_strategy[ts_code]['poom_1'] = flag_poom_1
                self._ts_code_to_strategy[ts_code]['poom_2'] = flag_poom_2

            except Exception as e:
                logger.warning(e)
          
    def get_ma_go_up(self):
        """
        args:
        return: 
            whether the stock is ma go up 
        """
        for ts_code, df in self._st_data.items():
            try:
                ret = self._ss.is_ma_go_up(df)

                self._ts_code_to_strategy[ts_code]['ma_sort_short'] = ret['ma_sort_short']
                self._ts_code_to_strategy[ts_code]['ma_sort_medium'] = ret['ma_sort_medium'] 
                self._ts_code_to_strategy[ts_code]['ma_sort_long'] = ret['ma_sort_long'] 
                self._ts_code_to_strategy[ts_code]['ma_short'] = ret['ma_short'] 
                self._ts_code_to_strategy[ts_code]['ma_medium'] = ret['ma_medium'] 
                self._ts_code_to_strategy[ts_code]['ma_long'] = ret['ma_long'] 
            except Exception as e:
                logger.warning(e)

    def get_vol_go_up(self):
        """
        args:
        return: 
            whether the stock is vol go up 
        """
        for ts_code, df in self._st_data.items():
            try:
                flag_vol = self._ss.is_vol_go_up(df)

                self._ts_code_to_strategy[ts_code]['vol'] = flag_vol 
            except Exception as e:
                logger.warning(e)

    def send_to_wechat(self, save=False):
        url_format = '{} https://xueqiu.com/S/{}\n\n'
        res = self.get_strategy_result()

        content = ''
        for k, v in self._mp.items():
            content += k 
            for ts_code, _ in res.items():
                if v in res[ts_code] and res[ts_code][v]== 1: 
                    name = self.get_ts_name_by_code(ts_code)
                    fields = ts_code.split('.')
                    content += url_format.format(name.encode('utf-8'), fields[1] + fields[0])
                    #content += url_format.format(name, fields[1] + fields[0])
        logger.debug('send_to_wechat: {}'.format(content))

        try:
            url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
            req = requests.post(url, data = {'text': 'Notice', 'desp': content})
        except Exception as e:
            logger.warning(e)

        if save == True:
            try:
                os.makedirs('result/')
            except Exception as e:
                logger.warning(e)
            
            today = datetime.date.today()
            today = today.strftime('%Y%m%d') + '.txt'

            file_name = 'result/' + today 
            fobj = open(file_name, 'w')
            fobj.write(content)
            fobj.close()


if __name__ == '__main__':
    stock = Stock()
    stock.init_data(['000001.SZ'])
    #stock.init_data()
    #stock.get_poom()
    #stock.get_ma_go_up()    
    #stock.get_vol_go_up()
    stock.send_to_wechat(save=True)
    
