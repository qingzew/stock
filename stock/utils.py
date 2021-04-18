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
def add_sma_indicator(df):
    #df['ma5'] = df['close'].ewm(span=5, adjust=False).mean() 
    #df['ma10'] = df['close'].ewm(span=10, adjust=False).mean() 
    #df['ma20'] = df['close'].ewm(span=20, adjust=False).mean() 
    #df['ma30'] = df['close'].ewm(span=30, adjust=False).mean() 
    #df['ma60'] = df['close'].ewm(span=60, adjust=False).mean() 
    try:
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma30'] = df['close'].rolling(window=30).mean()
        df['ma60'] = df['close'].rolling(window=60).mean()
    except:
        df['ma5'] = df['收盘价'].rolling(window=5).mean()
        df['ma10'] = df['收盘价'].rolling(window=10).mean()
        df['ma20'] = df['收盘价'].rolling(window=20).mean()
        df['ma30'] = df['收盘价'].rolling(window=30).mean()
        df['ma60'] = df['收盘价'].rolling(window=60).mean()

    df = df.fillna(0)
    return df



