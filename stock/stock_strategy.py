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
import math


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
        #charts.draw_charts(xaxis, stock_price, volume, dst_file, special_line=line)
        charts.draw_charts(xaxis, stock_price, volume, dst_file, slines=line)

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


def slope(st):
    """
    返回直线斜率。如果拟合误差大于err，则抛出异常
    """
    # 对st进行归一化，以便斜率可以在不同的时间序列之间进行比较
    norm = st[0] + 1e-6
    #norm = 1.
    st = st / norm
    x = np.arange(len(st))
    z = np.polyfit(x, st, deg=1)
    p = np.poly1d(z)

    st_hat = np.array([p(xi) for xi in x])
    line = np.array([float('{:.4f}'.format(p(xi) * norm)) for xi in x])
    error = rmse(st, st_hat) / np.sqrt(np.mean(np.square(st)))

    return np.degrees(np.arctan(z[0])), line, error


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

    #all_up = np.all([r > 1 and r < 1.05 for r in ratio]) 
    all_up = np.all([r > 1 for r in ratio]) 

    return all_up


def is_ma_up1(st, day):
    all_up1 = np.all(st['close'][-day:] > st['open'][-day:]) 
    all_up2 = np.all(st['close'][-day:] / st['close'][-day-1:-1] < 1.5) 

    return all_up1 and all_up2

def is_ma_up2(st, day):
    all_up1 = np.all(st['close'][-day:] > st['open'][-day:]) 
    all_up2 = np.all(st['close'][-day:] / st['close'][-day-1:-1] < 0.7) 

    return all_up1 and all_up2


def is_cross(st, day):
    o = st['open'].to_numpy()
    c = st['close'].to_numpy()
    l = st['low'].to_numpy()
    h = st['high'].to_numpy()
    ma5 = st['ma5'].to_numpy()
    
    # rise
    logger.info('open: {} close: {} {}'.format(o[-day:], c[-day:], all(o[-day:] < c[-day:])))
    if any(o[-day:] > c[-day:]):
        return False

    # upper/lower shallow
    main_diff = c[-day:] - o[-day:]
    up_diff = h[-day:] - c[-day:]
    down_diff = o[-day:] - l[-day:]
    logger.info('main diff: {} up diff: {} down diff: {}'.format(main_diff,up_diff, down_diff))
    if any(up_diff > main_diff) or any(down_diff > main_diff):
        return False

    logger.info('ma: {} open: {} ma: {}'.format(ma5[-day:] * 0.97, o[-day:], ma5[-day:] * 1.03))
    if not (all(o[-day:] >= ma5[-day:] * 0.97) and all(o[-day:] <= ma5[-day:] * 1.03)):
        return False

    # range
    logger.info('range: {}'.format((h[-1] - l[-1]) / l[-1]))
    if not (h[-1] - l[-1]) / l[-1] < 0.09:
        return False

    return True


def is_parallel(st, day):
    ma5 = st['ma5'][-day*5:].to_numpy()
    ma10 = st['ma10'][-day*5:].to_numpy()
    ma20 = st['ma20'][-day*5:].to_numpy()
    ma30 = st['ma30'][-day*5:].to_numpy()

    signal = (ma5 > ma10) & (ma10 >= ma20 * 0.98)
    run_values, run_starts, run_lengths = find_runs(signal)
    ma_parallel = run_values[-1] == True and run_lengths[-1] >= day

    logger.info('run_values: {} run_lengths: {}'.format(run_values, run_lengths))
    return ma_parallel

def is_volume(st, day):
    #try:
    volume = st['volume'][-day*5:].to_numpy()
    volume_flag = all(volume[-day:] / volume[-day-1] >= 1.2) and volume[-1] > 500000
    logger.info('volume: {}'.format(volume_flag))
    #except:
    #    volume_flag = False 

    return volume_flag

def is_slp5(st, day):
    ma5 = st['ma5'][-day*5:].to_numpy()
    date = st['date'][-day*5:].to_numpy()

    try:
        slp, l, err = slope(ma5[-day:])
        slp_flag5 = err < 0.1 and slp > 0.015 
        #line = {k: v for k, v in zip(date, line)}
        #line.append({k: v for k, v in zip(date[-len(l):], l)})
        line = {k: v for k, v in zip(date[-len(l):], l)}
    except:
        slp_flag5 = False
        line = {}
        err = 1e6

    logger.info('slp5: {}'.format(slp_flag5))
    return slp_flag5, line, err

def is_slp60(st, day):
    ma60 = st['ma60'][-60:].to_numpy()
    date = st['date'][-60:].to_numpy()
    try:
        slp, l, err = slope(ma60[-30:])
        slp_flag60 = err < 0.1 and slp > 0.
        #line.append({k: v for k, v in zip(date[-len(l):], l)})
        line = {k: v for k, v in zip(date[-len(l):], l)}
    except:
        slp_flag60 = False
        line = [] 
        err = 1e6

    logger.info('slp60: {}'.format(slp_flag60))
    return slp_flag60, line, err


def is_ratio(st, day):
    ma5 = st['ma5'][-day*5:].to_numpy()
    ma10 = st['ma10'][-day*5:].to_numpy()
    ma20 = st['ma20'][-day*5:].to_numpy()

    ratio1 = ma5[-1] / ma10[-1] 
    ratio2 = ma10[-1] / ma20[-1]
    ratio_flag = ratio1 > 1.01 and ratio2 >= 0.99 

    logger.info('ratio1: {} ratio2: {}'.format(ratio1, ratio2))
    return ratio_flag


class StockStrategy(object):
    """
    stock strategy
    """

    def __init__(self):
        """
        """

    @save_fig
    def is_ma_parallel(self, st, day, st_code=None, check_date=True):
        """
        :param st: 收盘价数组
        :params n: 多头排列刚形成day天
        """

        logger.info('\n{}{}{}'.format('#' * 50, st_code, '#' * 50))

        # ma parallel
        ma_parallel = is_parallel(st, day)

        # volume
        volume_flag = is_volume(st, day)

        # cross
        cross_flag = is_cross(st, day)

        lines = []
        slp_flag5, line, _ = is_slp5(st, day)
        lines.append(line)

        slp_flag60, line, err = is_slp60(st, day)
        lines.append(line)

        ratio_flag = is_ratio(st, day)
        

        if check_date:
            date = st['date'].to_numpy()
            last_trade = datetime.datetime.strptime(date[-1], '%Y-%m-%d').date()
            today = datetime.date.today()
            yestoday = datetime.date.today() - datetime.timedelta(days=1)

            date_flag = last_trade - today < datetime.timedelta(days=2)
        else:
            date_flag = True 

        final_flag = ma_parallel and cross_flag and volume_flag and slp_flag5 and slp_flag60 and date_flag and ratio_flag
        logger.info('code: {} final: {} ma_parallel: {} cross_flag: {} volume_flag: {} slp_flag5: {} slp_flag60: {} date_flag: {} ratio_flag: {}'.format(
                st_code, final_flag, ma_parallel, cross_flag, volume_flag, slp_flag5, slp_flag60, date_flag, ratio_flag))

        return final_flag, err, lines, st_code, st
    

if __name__ == '__main__':
    import os
    import pandas as pd

    st = StockStrategy()
    #root_dir = 'data/us'
    #root_dir = 'data/kcb'
    root_dir = 'data/a'
    final_res = []
    for f in os.listdir(root_dir):
        path = os.path.join(root_dir, f)
        st_code = f.split('.')[0]
        if st_code != 'sz002215':
            continue

        df = pd.read_csv(path)
        target_col = ['date', 'open', 'high', 'low', 'close', 'volume',
                'ma5', 'ma10', 'ma20', 'ma30', 'ma60']
        df = df[target_col]
        #df = df[:-1]
        #print(df)
        #res = st.is_ma_parallel(df, 2, st_code, check_date=True)
        try:
            res = st.is_ma_parallel(df, 2, st_code, check_date=True)
            if res[0]:
                final_res.append(f)
        except:
            pass

    for r in final_res:
        print(r)
