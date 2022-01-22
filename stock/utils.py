#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file utils.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""
target_col = ['date', 'open', 'high', 'low', 'close', 'volume',
        'ma5', 'ma10', 'ma20', 'ma30', 'ma60']

def add_sma(df, data_type='kcb'):

    if data_type == 'kcb':
        df.rename(columns={
                '日期': 'date', 
                '开盘价': 'open',  
                '最高价': 'high', 
                '最低价': 'low', 
                '收盘价': 'close',
                '成交': 'volume',
                '盘后量': '盘后量', 
                '盘后额': '盘后额'}, 
                inplace=True)
        for col in target_col[1:-5]:
            df[[col]] = df[[col]].astype('float64')
    else:
        df.reset_index(level=0, inplace=True)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ma30'] = df['close'].rolling(window=30).mean()
    df['ma60'] = df['close'].rolling(window=60).mean()

    df = df[target_col]
    return df

