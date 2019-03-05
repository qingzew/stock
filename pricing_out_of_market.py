#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the LGPL3 license.
###############################################################

"""
    @file pricing_out_of_market.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import datetime
import tushare as ts 

from base_obj import BaseObj
from logger import logger

class PricingOutOfMarket(BaseObj):
    def __init__(self):
        super(PricingOutOfMarket, self).__init__()

    # pricing out of market
    def is_pricing_out_of_market(self, st_data):

        """
        Args:
            st_data: stock price data in 10 consecutive days        

        Return:
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

        flag_1st = False
        if pct_change_0 > 9.95 and abs(low_price_0 - close_price_0) < 0.05:
            if abs(low_price_1 - high_price_1) > 0.1:
                flag_1st = True
            else: 
                logger.debug('1st {} {} fail'.format(ts_code, trade_date_1))
        else:
            logger.debug('1st {} {} fail'.format(ts_code, trade_date_0))

        flag_2ed = False
        if pct_change_0 > 9.95 and abs(low_price_0 - close_price_0) < 0.05:
            if pct_change_1 > 9.95 and abs(low_price_1 - close_price_1) < 0.05:
                #if pct_change_2 <= 0.98 and low_price_2 < high_price_2:
                    #if vol_0 < vol_1 and vol_1 < vol2:
                    #    return True
                if abs(low_price_2 - high_price_2) > 0.1:
                    flag_2ed = True
                else: 
                    logger.debug('2ed {} {} fail'.format(ts_code, trade_date_2))
            else:
                logger.debug('2ed {} {} fail'.format(ts_code, trade_date_1))
        else: 
            logger.debug('2ed {} {} fail'.format(ts_code, trade_date_0))

        return flag_1st, flag_2ed


    def get_pricing_out_of_market(self):
        """
        Args:
        Return:
            1st_pricing_out_of_market: stocks pricing out of market firstly
            2ed_pricing_out_of_market: stocks pricing out of market secondly
        """
        pro = ts.pro_api('95f7a4bf060e97230010a4287cf6db5a5e58c4deadef29f31d966978')
    
        #today = datetime.date.today()
        #today = today.strftime('%Y%m%d')
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y%m%d')
        end_date = datetime.date.today().strftime('%Y%m%d')
        #today = today.strftime('%Y%m%d')
        trade_cal = pro.trade_cal(exchange='', start_date=start_date, end_date=end_date)
        trade_cal = trade_cal[::-1]
        include_days = []
        for idx, row in trade_cal.iterrows():
            if row['is_open'] == 1:
                include_days.append(row['cal_date'])

            if len(include_days) == 10:
                break

        pricing_out_of_market_1st = []
        pricing_out_of_market_2ed = []
        for ts_code in self.ts_codes:
            try:
            	df = ts.pro_bar(pro_api=pro, 
            	    ts_code=ts_code, 
            	    asset='E', 
            	    start_date=include_days[-1], 
            	    end_date=include_days[0], 
            	    freq='D',
            	    adj='qfq')

                flag_1st, flag_2ed = self.is_pricing_out_of_market(df)
                if flag_1st:
                    pricing_out_of_market_1st.append([ts_code, self.ts_codes_to_name[ts_code]])

                if flag_2ed:
                    pricing_out_of_market_2ed.append([ts_code, self.ts_codes_to_name[ts_code]])
            except Exception as e:
                print e

        return pricing_out_of_market_1st, pricing_out_of_market_2ed

if __name__ == '__main__':
    poom = PricingOutOfMarket()
    print poom.get_pricing_out_of_market()


