#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file hot_stock.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""
import dtshare as dt


def get_weibo_hot():
    df = dt.stock_js_weibo_report(time_period="CNDAY7")
    return df

