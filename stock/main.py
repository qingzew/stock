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
import gc

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', help='run the script', action='store_true')
parser.add_argument('-A', '--alljob', help='test the script', action='store_true')
parser.add_argument('-ja', '--joba', help='test the script', action='store_true')
parser.add_argument('-jh', '--jobhk', help='test the script', action='store_true')
parser.add_argument('-ju', '--jobus', help='test the script', action='store_true')
args = parser.parse_args()


stock = Stock()

def a_job():
    logger.info('init stock data...')

    stock.get_data_a()
    stock.get_ma30_go_up_a()
    stock.send_to_wechat(st_type='a')


def kcb_job():
    logger.info('init stock data...')

    stock.get_data_kcb()
    stock.get_ma30_go_up_kcb()
    stock.send_to_wechat(st_type='kcb')


def us_job():
    logger.info('init stock data...')

    stock.get_data_us()
    stock.get_ma30_go_up_us()
    stock.send_to_wechat(st_type='us')


def hk_job():
    logger.info('init stock data...')

    stock.get_data_hk()
    stock.get_ma30_go_up_hk()
    stock.send_to_wechat(st_type='hk')

def job_a():
    a_job()
    kcb_job()

def job_hk():
    hk_job()

def job_us():
    us_job()

if __name__ == '__main__':
    print(args)
    if args.run:
         sched = BlockingScheduler()
         #sched.add_job(a_job, 'cron', day_of_week='mon-fri',  hour=17, minute=00)
         #sched.add_job(hk_job, 'cron', day_of_week='mon-fri',  hour=20, minute=00)
         #sched.add_job(us_job, 'cron', day_of_week='mon-sat',  hour=8, minute=30)
         sched.add_job(job_a, 'cron', day_of_week='mon-fri',  hour=17, minute=00)
         sched.add_job(job_b, 'cron', day_of_week='mon-sat',  hour=6, minute=00)
         sched.start()
    elif args.alljob:
         logger.info('a job...')
         a_job()
         logger.info('kcb job...')
         kcb_job()
         logger.info('us job...')
         us_job()
         logger.info('hk job...')
         hk_job()
    elif args.joba:
         logger.info('a job...')
         a_job()
         kcb_job()
    elif args.jobhk:
         logger.info('hk job...')
         hk_job()
    elif args.jobus:
         logger.info('hk job...')
         us_job()

    else:
        print('usage: main.py [-h] [-r] [-t]')


