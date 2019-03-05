#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the LGPL3 license.
###############################################################

"""
    @file main.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""


import os
import datetime
import codecs
from apscheduler.schedulers.blocking import BlockingScheduler
from pricing_out_of_market import PricingOutOfMarket
from logger import logger

def job():
    poom = PricingOutOfMarket()
    poom_1st, poom_2ed = poom.get_pricing_out_of_market()

    try:
        os.makedirs('result/')
    except Exception as e:
	logger.warning(e)

    today = datetime.date.today()
    today = today.strftime('%Y%m%d') + '.txt'
    fobj = open('./result/' + today, 'w')

    url_format = '{} https://xueqiu.com/S/{}\n'

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


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(job, 'cron', day_of_week='mon-fri',  hour=18, minute=0)
    sched.start()


