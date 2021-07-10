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
from collections import OrderedDict, defaultdict
import pandas as pd
from pandas import Series, DataFrame
from logger import logger

from stock_data_a import StockData as StockDataA
from stock_data_kcb import StockData as StockDataKCB
from stock_data_us import StockData as StockDataUS
from stock_data_hk import StockData as StockDataHK
from stock_strategy import StockStrategy
from hot_stock import get_weibo_hot

class Stock(object):
    """
    call StockData and StockStrategy to predict stock
    """

    def __init__(self):
        """
        """
     
        self._sd_a = StockDataA()
        self._st_data_a = defaultdict(DataFrame)

        self._sd_kcb = StockDataKCB()
        self._st_data_kcb = defaultdict(DataFrame)
       
        self._sd_us = StockDataUS()
        self._st_data_us = defaultdict(DataFrame)

        self._sd_hk = StockDataHK()
        self._st_data_hk = defaultdict(DataFrame)

        self._mp_a = OrderedDict([
                #('###一字板\n\n', 'poom_1st'),
                #('###二字板\n\n', 'poom_2ed'),
                #('###ma5&10&20长排列\n\n', 'ma_sort_short'),
                #('###ma5&10&20&30长排列\n\n', 'ma_sort_medium'),
                #('###ma5&10&20&30&60长排列\n\n', 'ma_sort_long'),
                #('###ma5&10&20短排列\n\n', 'ma_short'),
                #('###ma5&10&20&30短排列\n\n', 'ma_medium'),
                #('###ma5&10&20&30&60短排列\n\n', 'ma_long'),
                ('###ma30_a\n\n', 'ma30_a'),
                ])
        self._mp_kcb = OrderedDict([
                ('###ma30_kcb\n\n', 'ma30_kcb'),
                ])

        self._mp_us = OrderedDict([
                ('###ma30_us\n\n', 'ma30_us'),
                ])

        self._mp_hk = OrderedDict([
                ('###ma30_hk\n\n', 'ma30_hk'),
                ])

        self._ss = StockStrategy()
        self._symbol_to_strategy_a = defaultdict(lambda: defaultdict(lambda:0))
        self._symbol_to_strategy_kcb = defaultdict(lambda: defaultdict(lambda:0))
        self._symbol_to_strategy_us = defaultdict(lambda: defaultdict(lambda:0))
        self._symbol_to_strategy_hk = defaultdict(lambda: defaultdict(lambda:0))

    def get_data_a(self):
        symbols = self._sd_a.get_symbols()
        for symbol in symbols:
            try:
                df = self._sd_a.get_df_by_symbol(symbol)
                self._st_data_a[symbol] = df
            except Exception as e:
                logger.warning(e)

    def get_data_kcb(self):
        symbols = self._sd_kcb.get_symbols()
        for symbol in symbols:
            try:
                df = self._sd_kcb.get_df_by_symbol(symbol)
                self._st_data_kcb[symbol] = df
            except Exception as e:
                logger.warning(e)

    def get_data_us(self):
        symbols = self._sd_us.get_symbols()
        for symbol in symbols:
            try:
                df = self._sd_us.get_df_by_symbol(symbol)
                self._st_data_us[symbol] = df
            except Exception as e:
                logger.warning(e)

    def get_data_hk(self):
        symbols = self._sd_hk.get_symbols()
        for symbol in symbols:
            #try:
            #    df = self._sd_hk.get_df_by_symbol(symbol)
            #    self._st_data_hk[symbol] = df
            #except Exception as e:
            #    logger.warning(e)
            df = self._sd_hk.get_df_by_symbol(symbol)
            self._st_data_hk[symbol] = df

    def get_one_data(self, symbol_a=None, symbol_kcb=None, 
            symbol_us=None, symbol_hk=None, days=90):
        """
        get stock data for once
        args:
        return:
            basic datas for specified stock
        """
        if symbol_a is not None:
            try:
                df = self._sd_a.get_df_by_symbol(symbol_a)
                self._st_data_a[symbol_a] = df
            except Exception as e:
                logger.warning(e)

        if symbol_kcb is not None:
            try:
                df = self._sd_kcb.get_df_by_symbol(symbol_kcb)
                self._st_data_kcb[symbol_kcb] = df
            except Exception as e:
                logger.warning(e)

        if symbol_us is not None:
            try:
                df = self._sd_us.get_df_by_symbol(symbol_us)
                self._st_data_us[symbol_us] = df
            except Exception as e:
                logger.warning(e)

        if symbol_hk is not None:
            try:
                df = self._sd_hk.get_df_by_symbol(symbol_hk)
                self._st_data_hk[symbol_hk] = df
            except Exception as e:
                logger.warning(e)

    def get_st_name_by_symbol_a(self, symbol):
        symbol_to_name = self._sd_a.get_symbol_to_name() 
        return symbol_to_name[symbol]

    def get_st_name_by_symbol_kcb(self, symbol):
        symbol_to_name = self._sd_kcb.get_symbol_to_name() 
        return symbol_to_name[symbol]

    def get_st_name_by_symbol_us(self, symbol):
        symbol_to_name = self._sd_us.get_symbol_to_name() 
        return symbol_to_name[symbol]

    def get_st_name_by_symbol_hk(self, symbol):
        symbol_to_name = self._sd_hk.get_symbol_to_name() 
        return symbol_to_name[symbol]
   
    def get_strategy_result_a(self):
        return self._symbol_to_strategy_a

    def get_strategy_result_kcb(self):
        return self._symbol_to_strategy_kcb

    def get_strategy_result_us(self):
        return self._symbol_to_strategy_us

    def get_strategy_result_hk(self):
        return self._symbol_to_strategy_hk

    #def get_poom(self):
    #    """
    #    args:
    #    returns:
    #        whether the stock is pricing out of market
    #    """
    #    for ts_code, df in self._st_data.items():
    #        try:
    #            flag_poom_1st, flag_poom_2ed, flag_poom_1, flag_poom_2 = \
    #                    self._ss.is_pricing_out_of_market(df)
    #            
    #            self._symbol_to_strategy[ts_code]['poom_1st'] = flag_poom_1st
    #            self._symbol_to_strategy[ts_code]['poom_2ed'] = flag_poom_2ed
    #            self._symbol_to_strategy[ts_code]['poom_1'] = flag_poom_1
    #            self._symbol_to_strategy[ts_code]['poom_2'] = flag_poom_2

    #        except Exception as e:
    #            logger.warning(e)
    #      
    #def get_ma_go_up(self):
    #    """
    #    args:
    #    return: 
    #        whether the stock is ma go up 
    #    """
    #    for ts_code, df in self._st_data.items():
    #        try:
    #            ret = self._ss.is_ma_go_up(df)

    #            self._symbol_to_strategy[ts_code]['ma_sort_short'] = ret['ma_sort_short']
    #            self._symbol_to_strategy[ts_code]['ma_sort_medium'] = ret['ma_sort_medium'] 
    #            self._symbol_to_strategy[ts_code]['ma_sort_long'] = ret['ma_sort_long'] 
    #            self._symbol_to_strategy[ts_code]['ma_short'] = ret['ma_short'] 
    #            self._symbol_to_strategy[ts_code]['ma_medium'] = ret['ma_medium'] 
    #            self._symbol_to_strategy[ts_code]['ma_long'] = ret['ma_long'] 
    #        except Exception as e:
    #            logger.warning(e)
    #
    #def get_vol_go_up(self):
    #    """
    #    args:
    #    return: 
    #        whether the stock is vol go up 
    #    """
    #    for ts_code, df in self._st_data.items():
    #        try:
    #            ma30_flag = self._ss.is_vol_go_up(df)

    #            self._symbol_to_strategy[ts_code]['vol'] = flag_vol 
    #        except Exception as e:
    #            logger.warning(e)

    def get_ma30_go_up_a(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_a.items():
            try:
                flag = self._ss.is_ma30_go_up(symbol, df)
                self._symbol_to_strategy_a[symbol]['ma30_a'] = flag 
            except Exception as e:
                logger.warning(e)

    def get_ma30_go_up_kcb(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_kcb.items():
            try:
                flag = self._ss.is_ma30_go_up(symbol, df)
                self._symbol_to_strategy_kcb[symbol]['ma30_kcb'] = flag 
            except Exception as e:
                logger.warning(e)

    def get_ma30_go_up_us(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_us.items():
            try:
                flag = self._ss.is_ma30_go_up(symbol, df)
                self._symbol_to_strategy_us[symbol]['ma30_us'] = flag 
            except Exception as e:
                logger.warning(e)

    def get_ma30_go_up_hk(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_hk.items():
            try:
                flag = self._ss.is_ma30_go_up(symbol, df)
                self._symbol_to_strategy_hk[symbol]['ma30_hk'] = flag 
            except Exception as e:
                logger.warning(e)

    def send_message( 
            self,
            content, 
            token='', 
            summary='stock msg',
            topic_ids=[2544], 
            content_type=3, 
            uids=[],
            msg_url=''):
        """Send Message."""
        msg = {
                'appToken': token,
                'summary': summary, 
                'content': content,
                'contentType': content_type,
                'topicIds': topic_ids,
                'uids': uids,
                'url': msg_url
            }

        url = 'http://wxpusher.zjiecode.com/api/send/message'

        return requests.post(url, json=msg).json()


    def send_to_wechat(self, st_type='a', save=False):
        url_format = '{} https://xueqiu.com/S/{}\n\n'
        mp = {
                'a': 'a股',
                'kcb': '科创',
                'us': '美股',
                'hk': '港股'
                }

        if st_type == 'a':
            content = ''
            res_a = self.get_strategy_result_a()
            for k, v in self._mp_a.items():
                content += k 
                for symbol, _ in res_a.items():
                    if v in res_a[symbol] and res_a[symbol][v]== 1: 
                        name = self.get_st_name_by_symbol_a(symbol)
                        content += url_format.format(name, symbol.upper())

        if st_type == 'kcb':
            content = ''
            res_kcb = self.get_strategy_result_kcb()
            for k, v in self._mp_kcb.items():
                content += k 
                for symbol, _ in res_kcb.items():
                    if v in res_kcb[symbol] and res_kcb[symbol][v]== 1: 
                        name = self.get_st_name_by_symbol_kcb(symbol)
                        content += url_format.format(name, symbol.upper())

        if st_type == 'us':
            content = ''
            res_us = self.get_strategy_result_us()
            for k, v in self._mp_us.items():
                content += k 
                for symbol, _ in res_us.items():
                    if v in res_us[symbol] and res_us[symbol][v]== 1: 
                        name = self.get_st_name_by_symbol_us(symbol)
                        content += url_format.format(name, symbol.upper())


        if st_type == 'hk':
            content = ''
            res_hk = self.get_strategy_result_hk()
            for k, v in self._mp_hk.items():
                content += k 
                for symbol, _ in res_hk.items():
                    if v in res_hk[symbol] and res_hk[symbol][v]== 1: 
                        name = self.get_st_name_by_symbol_hk(symbol)
                        content += url_format.format(name, symbol.upper())

        logger.debug('send_to_wechat: {}'.format(content))

        #cnt = 10
        #while cnt != 0:
        #    try:
        #        url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
        #        req = requests.post(url, data = {'text': mp[st_type], 'desp': content})
        #        break
        #    except Exception as e:
        #        logger.warning('error to send to wechat {}'.format(e))
        #        cnt -= 1

        cnt = 10
        while cnt != 0:
            ret = self.send_message(summary=mp[st_type], content=content)
            if ret['code'] == 1000:
                break

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


    def send_hot_to_wechat(self):
        url_format = '{} https://xueqiu.com/S/{}\n\n'
        st_name_to_symbol = {}
        symbol_to_name_a = self._sd_a.get_symbol_to_name()
        for k, v in symbol_to_name_a.items():
            st_name_to_symbol[v] = k

        df = get_weibo_hot()
        content = ''
        for _, row in df.iterrows():
            print(row['name'])
            content += url_format.format(st_name_to_symbol[row['name']])

        cnt = 10
        while cnt != 0:
            try:
                url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
                req = requests.post(url, data = {'text': 'Hotspot', 'desp': content})
                break
            except Exception as e:
                logger.warning('error to send to wechat {}'.format(e))
                cnt -= 1

        

if __name__ == '__main__':
    stock = Stock()
    #stock.init_data(['AMZN'])
    #stock.init_data()
    #stock.get_poom()
    #stock.get_ma_go_up()    
    #stock.get_vol_go_up()
    #stock.get_one_data(ts_code='000001.SZ', us_ts_code='AAPL', days=90)
    stock.get_one_data(symbol_a='000001.SZ', symbol_us='AAPL', symbol_hk='00003', days=90)

    stock.get_ma30_go_up_a()
    stock.send_to_wechat(st_type='a')

    #stock.get_ma30_go_up_us()
    #stock.send_to_wechat(st_type='us')

    #stock.get_ma30_go_up_hk()
    #stock.send_to_wechat(st_type='hk')
    #stock.send_hot_to_wechat()
