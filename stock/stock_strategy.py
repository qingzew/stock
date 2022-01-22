#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Righst Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file stock_strategy.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import os
import datetime
from collections import OrderedDict, defaultdict
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

from logger import logger
import functools
import charts


def save_fig(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        flag, err, line, st_code, st = func(*args, **kwargs)

        st_np = st.to_numpy()[-100:]
        xaxis = []
        stock_price = []
        volume = []
        for row in st_np:
            d, o, h, l, c, v = row[0], row[1], row[2], row[3], row[4], row[5]
            xaxis.append(d)
            stock_price.append([o, c, l, h])
            volume.append(v)

        try:
            os.makedirs('figs')
        except:
            pass
        dst_file = os.path.join('figs', str(st_code) + '.html')
        charts.draw_charts(xaxis, stock_price, volume, dst_file, special_line=line)

        return flag, err
    return wrapper_func


def rmse(y, y_hat):
    """
    返回预测序列相对于真值序列的标准差。
    Args:
        y:
        y_hat:

    Returns:

    """
    return np.sqrt(np.mean(np.square(y - y_hat)))


#def slope(st, err):
def slope(st):
    """
    返回直线斜率。如果拟合误差大于err，则抛出异常
    """
    # 对st进行归一化，以便斜率可以在不同的时间序列之间进行比较
    #assert st[0] != 0
    norm = st[0] + 1e-6
    st = st / norm
    x = np.arange(len(st))
    z = np.polyfit(x, st, deg=1)
    p = np.poly1d(z)

    line = np.array([float('{:.4f}'.format(p(xi) * norm)) for xi in x])
    st_hat = np.array([p(xi) for xi in x])
    error = rmse(st, st_hat) / np.sqrt(np.mean(np.square(st)))
    #if error >= err:
    #    #raise ValueError("can not fit into line, error: {}".format(error))
    #    z = []
    #    line = [] 
    #    error = 1e6

    return z[0], line, error


def moving_average(st, win):
    st_np = st.to_numpy().astype(np.float32)
    return np.convolve(st_np, np.ones(win) / win, 'valid')


def find_runs(x):
    """Find runs of consecutive items in an array."""

    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError('only 1D array supported')
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starst
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])

        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_starts, run_lengths

def is_ma_up(ma, close):
    ratio = close / ma

    all_up = np.all([r > 1 and r < 1.05 for r in ratio]) 

    return all_up


def is_ma_up1(st, day):
    all_up1 = np.all(st['close'][-day:] > st['open'][-day:]) 
    all_up2 = np.all(st['close'][-day:] / st['close'][-day-1:-1] < 1.5) 

    return all_up1 and all_up2

def is_ma_up2(st, day):
    all_up1 = np.all(st['close'][-day:] > st['open'][-day:]) 
    all_up2 = np.all(st['close'][-day:] / st['close'][-day-1:-1] < 0.7) 

    return all_up1 and all_up2


class StockStrategy(object):
    """
    stock strategy
    """

    def __init__(self):
        """
        """

    @save_fig
    def is_ma_parallel(self, st, day, st_code=None, check_date=False):
        """
        :param st: 收盘价数组
        :params n: 多头排列刚形成day天
        """

        inter = 200 
        ma5 = st['ma5'][-inter:].to_numpy()
        ma10 = st['ma10'][-inter:].to_numpy()
        ma20 = st['ma20'][-inter:].to_numpy()
        ma30 = st['ma30'][-inter:].to_numpy()
        close = st['close'][-inter:].to_numpy()
        date = st['date'][-day:].to_numpy()

        # ma parallel
        signal = (ma5 > ma10) & (ma10 > ma20)
        run_values, run_starts, run_lengths = find_runs(signal)
        ma_parallel = run_values[-1] == True and run_lengths[-1] >= day
        print(run_values)
        print(run_lengths)

        # close > open
        ma_up1 = is_ma_up(ma5[-day:], close[-day:]) 

        # go up for a long time 
        #idx = inter // 3 if inter // 3 < len(st) else len(st)
        #ma_up2 = True if ma5[-idx] < ma5[-1] else False
        ma_up2 = True

        # volume
        volume_flag = st['volume'].to_numpy()[-1] > 5000000

        # with a slope
        #slp, line, err = slope(ma5[-day:], 0.1)
        #slp_flag = slp is not None and slp < 0.05 and slp > 0.015 
        try:
            slp, line, err = slope(ma5[-day:])
            slp_flag = err < 0.1 and slp > 0.015 
            line = {k: v for k, v in zip(date, line)}
        except:
            slp_flag = False
            line = {}
            err = 1e6

        if check_date:
            date_flag = date[-1] == datetime.date.today()
        else:
            date_flag = True 


        final_flag = ma_parallel & ma_up1 & ma_up2 & slp_flag & date_flag
        logger.info('code: {} {} ma_parallel: {} ma_up1: {} ma_up2:{}  volume_flag: {} slp_flag: {} date_flag: {}'.format(
                st_code, final_flag, ma_parallel, ma_up1, ma_up2, volume_flag, slp_flag, date_flag))


        return final_flag, err, line, st_code, st
    

if __name__ == '__main__':
    import os
    import pandas as pd

    st = StockStrategy()
    #root_dir = 'data/us'
    #root_dir = 'data/kcb'
    root_dir = 'data/a'
    for f in os.listdir(root_dir):
        path = os.path.join(root_dir, f)
        st_code = f.split('.')[0]

        if st_code != 'sz000963':
            continue
        df = pd.read_csv(path)
        st.is_ma_parallel(df, 10, st_code, check_date=False)

        break
