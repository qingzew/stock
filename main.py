#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the GPL3 license.
###############################################################

"""
    @file main.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""


import os
import codecs
import requests
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from logger import logger
from stock import Stock 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', help='run the script', action='store_true')
parser.add_argument('-t', '--test', help='test the script', action='store_true')
args = parser.parse_args()

def job():
    try:
        os.makedirs('result/')
    except Exception as e:
        logger.warning(e)

    today = datetime.date.today()
    today = today.strftime('%Y%m%d') + '.txt'

    url_format = '{} https://xueqiu.com/S/{}\n'

    stock = Stock()
    logger.info('init stock data...')
    #stock.init_data('000001.SZ')
    stock.init_data()
    logger.info('call stock strategy...')

    files = []

    poom_1st, poom_2ed = stock.get_poom() 

    file_name = './result/poom_' + today
    fobj = open(file_name, 'w')
    title = u'##首板'
    fobj.write('{}\n'.format(title.encode('utf-8')))
    for code, name in poom_1st:
        fields = code.split('.')
        fobj.write(url_format.format(name.encode('utf-8'), fields[1] + fields[0]))

    title = u'##二连板'
    fobj.write('{}\n'.format(title.encode('utf-8')))
    for code, name in poom_2ed:
        fields = code.split('.')
        fobj.write(url_format.format(name.encode('utf-8'), fields[1] + fields[0]))

    fobj.close()
    files.append(file_name)

    ma_go_up = stock.get_ma_go_up()

    file_name = './result/ma_' + today
    fobj = open(file_name, 'w')
    title = u'##多头排列'
    fobj.write('{}\n'.format(title.encode('utf-8')))
    for code, name in ma_go_up:
        fields = code.split('.')
        fobj.write(url_format.format(name.encode('utf-8'), fields[1] + fields[0]))

    fobj.close()
    files.append(file_name)

    # send to wechat
    msgs = ''
    for file_name in files:
        lines = codecs.open(file_name, 'r', 'utf-8').readlines()
        for line in lines:
            msgs += line.strip() + '\n\n'

    logger.info('send to wechat...')
    try:
        url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
        req = requests.post(url, data = {'text': 'Notice', 'desp': msgs})
    except Exception as e:
        logger.warning(e)


if __name__ == '__main__':
    if args.run:
        sched = BlockingScheduler()
        sched.add_job(job, 'cron', day_of_week='mon-fri',  hour=15, minute=0)
        sched.start()
    elif args.test:
        logger.info('testing...')
        job()
    else:
        print('usage: main.py [-h] [-r] [-t]')


