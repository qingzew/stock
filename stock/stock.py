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

from stock_data_zh import StockData as StockDataA
from stock_data_kcb import StockData as StockDataKCB
from stock_data_us import StockData as StockDataUS
from stock_data_hk import StockData as StockDataHK
from stock_strategy import StockStrategy
from stock_strategy import StockStrategy as StockStrategyV2
from hot_stock import get_weibo_hot

work_dir = os.path.dirname(os.path.realpath(__file__))
#url_format = '{}\n https://xueqiu.com/S/{}\n\n'
url_format = '[{}](https://xueqiu.com/S/{})\n\n'

p_day = 5

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

        self._ss_v2 = StockStrategyV2()

    def get_data_zh(self):
        symbols = self._sd_a.get_symbols()
        for symbol in symbols:
            logger.info('{} get data'.format(symbol))
            try:
                df = self._sd_a.get_df_by_symbol(symbol)
                self._st_data_a[symbol] = df
                
                dst_dir = os.path.join(work_dir, 'data', 'a')
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                df[-200:].to_csv(os.path.join(dst_dir, symbol + '.csv'))
                    
            except Exception as e:
                logger.error('{} get data error: {}'.format(symbol, e))

        return self._st_data_a

    def get_data_kcb(self):
        symbols = self._sd_kcb.get_symbols()
        for symbol in symbols:
            logger.info('{} get data'.format(symbol))
            try:
                df = self._sd_kcb.get_df_by_symbol(symbol)
                self._st_data_kcb[symbol] = df

                dst_dir = os.path.join(work_dir, 'data', 'kcb')
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                df[-200:].to_csv(os.path.join(dst_dir, symbol + '.csv'))

            except Exception as e:
                logger.error('{} get data error: {}'.format(symbol, e))

        return self._st_data_kcb

    def get_data_us(self):
        symbols = self._sd_us.get_symbols()
        for symbol in symbols:
            logger.info('{} get data'.format(symbol))
            try:
                df = self._sd_us.get_df_by_symbol(symbol)
                self._st_data_us[symbol] = df

                dst_dir = os.path.join(work_dir, 'data', 'us')
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                df[-200:].to_csv(os.path.join(dst_dir, symbol + '.csv'))

            except Exception as e:
                logger.error('{} get data error: {}'.format(symbol, e))

        logger.info('#' * 100)
        logger.info('total: {}'.format(len(self._st_data_us)))

        return self._st_data_us

    def get_data_hk(self):
        symbols = self._sd_hk.get_symbols()
        for symbol in symbols:
            logger.info('{} get data'.format(symbol))
            try:
                df = self._sd_hk.get_df_by_symbol(symbol)
                self._st_data_hk[symbol] = df

                dst_dir = os.path.join(work_dir, 'data', 'hk')
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                df[-200:].to_csv(os.path.join(dst_dir, symbol + '.csv'))

            except Exception as e:
                logger.error('{} get data error: {}'.format(symbol, e))

        return self._st_data_hk

    def get_one_data(self, symbol_a=None, symbol_kcb=None, 
            symbol_us=None, symbol_hk=None, days=90):
        """
        get stock data for once
        args:
        return:
            basic datas for specified stock
        """
        if symbol_a is not None:
            df = self._sd_a.get_df_by_symbol(symbol_a)
            self._st_data_a[symbol_a] = df

        if symbol_kcb is not None:
            df = self._sd_kcb.get_df_by_symbol(symbol_kcb)
            self._st_data_kcb[symbol_kcb] = df

        if symbol_us is not None:
            df = self._sd_us.get_df_by_symbol(symbol_us)
            self._st_data_us[symbol_us] = df

        if symbol_hk is not None:
            df = self._sd_hk.get_df_by_symbol(symbol_hk)
            self._st_data_hk[symbol_hk] = df

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

    def get_ma30_go_up_zh(self):
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

    def get_ma20_flag_zh(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_a.items():
            try:
                flag = self._ss_v2.is_ma20_up_with_slope(df, 5)
                self._symbol_to_strategy_a[symbol]['ma20_a'] = flag 

                logger.info('{} ma20: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

    def get_ma_parallel_flag_zh(self):
        """
        args:
        return: 
        """
        res = []
        for symbol, df in self._st_data_a.items():
            try:
                flag, err = self._ss_v2.is_ma_parallel(df, p_day, symbol)
                if flag:
                    name = self.get_st_name_by_symbol_a(symbol)
                    res.append([symbol, name, err])
                   
                logger.info('{} ma parallel: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

        res = sorted(res, key=lambda items: items[2])

        if len(res) > 0:
            self._send_message(summary='a股', content=res)

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

    def get_ma20_flag_kcb(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_kcb.items():
            try:
                flag = self._ss_v2.is_ma20_up_with_slope(df, 5)
                self._symbol_to_strategy_kcb[symbol]['ma20_kcb'] = flag 

                logger.info('{} ma20: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

    def get_ma_parallel_flag_kcb(self):
        """
        args:
        return: 
        """
        res = []
        for symbol, df in self._st_data_kcb.items():
            #try:
            flag, err = self._ss_v2.is_ma_parallel(df, p_day, symbol)
            if flag:
                name = self.get_st_name_by_symbol_kcb(symbol)
                res.append([symbol, name, err])
               
            logger.info('{} ma parallel: {}'.format(symbol, flag))
            #except Exception as e:
            #    logger.error('{} get flag error: {}'.format(symbol, e))

        res = sorted(res, key=lambda items: items[2])

        if len(res) > 0:
            self._send_message(summary='科创板', content=res)

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

    def get_ma20_flag_us(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_us.items():
            try:
                flag = self._ss_v2.is_ma20_up_with_slope(df, 5)
                self._symbol_to_strategy_us[symbol]['ma20_us'] = flag 

                logger.info('{} ma20: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

    def get_ma_parallel_flag_us(self):
        """
        args:
        return: 
        """
        res = []
        for symbol, df in self._st_data_us.items():
            try:
                flag, err = self._ss_v2.is_ma_parallel(df, p_day, symbol)
                if flag:
                    name = self.get_st_name_by_symbol_us(symbol)
                    res.append([symbol, name, err])
                   
                logger.info('{} ma parallel: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

        res = sorted(res, key=lambda items: items[2])

        if len(res) > 0:
            self._send_message(summary='美股', content=res)


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


    def get_ma20_flag_hk(self):
        """
        args:
        return: 
        """
        for symbol, df in self._st_data_hk.items():
            try:
                flag = self._ss_v2.is_ma20_up_with_slope(df, 5)
                self._symbol_to_strategy_hk[symbol]['ma20_hk'] = flag 

                logger.info('{} ma20: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

    def get_ma_parallel_flag_hk(self):
        """
        args:
        return: 
        """
        res = []
        for symbol, df in self._st_data_hk.items():
            try:
                flag, err = self._ss_v2.is_ma_parallel(df, p_day, symbol)
                if flag:
                    name = self.get_st_name_by_symbol_hk(symbol)
                    res.append([symbol, name, err])
                   
                logger.info('{} ma parallel: {}'.format(symbol, flag))
            except Exception as e:
                logger.error('{} get flag error: {}'.format(symbol, e))

        res = sorted(res, key=lambda items: items[2])

        if len(res) > 0:
            self._send_message(summary='港股', content=res)

    def _send_message( 
            self,
            content, 
            token='AT_Mp6haTsQAr12pcBmpoBNEMrPhRZEwt66', 
            summary='stock msg',
            topic_ids=[2544], 
            content_type=3, 
            uids=[],
            msg_url=''):
        """Send Message."""

        format_content = ''
        for c in content:
            symbol = c[0]
            name = c[1]
            format_content += url_format.format(name, symbol.upper())

        msg = {
                'appToken': token,
                'summary': summary, 
                'content': format_content,
                'contentType': content_type,
                'topicIds': topic_ids,
                'uids': uids,
                'url': msg_url
            }

        url = 'http://wxpusher.zjiecode.com/api/send/message'
        for i in range(10):
            ret = requests.post(url, json=msg).json()
            if ret['code'] == 1000:
               break 
            logger.warn(ret)

        

if __name__ == '__main__':
    stock = Stock()
    stock.get_one_data(symbol_a='sz300895', symbol_kcb='sh688091', 
                symbol_us='ASML', symbol_hk='00003', days=90)

    #stock.get_ma20_flag_zh()
    stock.get_ma_parallel_flag_zh()
    #stock.send_to_wechat(st_type='a')

    #stock.get_ma20_flag_kcb()
    stock.get_ma_parallel_flag_kcb()
    #stock.send_to_wechat(st_type='kcb')

    #stock.get_ma20_flag_hk()
    stock.get_ma_parallel_flag_hk()
    #stock.send_to_wechat(st_type='hk')

    #stock.get_ma20_flag_us()
    stock.get_ma_parallel_flag_us()
    #stock.send_to_wechat(st_type='hk')

    pass
