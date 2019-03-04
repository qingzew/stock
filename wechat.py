#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

###############################################################
# Copyright (C) 2019 your company All Rights Reserved
#
# Distributed under terms of the LGPL3 license.
###############################################################

"""
    @file wechat.py
    @author wangqingze
    @date 2019-03-04 10:24
    @brief
"""

import os
import time
import codecs
import requests
#import itchat
from itchat.content import *
import hashlib

md5 = None
file_to_check = 'candidate_stocks.txt'

while 1:
    try:
        #msgs = codecs.open(file_to_check, 'r', 'utf-8').readlines()
        msgs = codecs.open(file_to_check, 'r', 'utf-8').read()
        cur_md5 = hashlib.md5(msgs).hexdigest()

        if cur_md5 == md5:
            print '{} has no changes, waiting 30min'.format(file_to_check)
            #time.sleep(30 * 60)
            time.sleep(3)
            continue
        else:
            md5 = cur_md5

        print 'sending msg...'

        #msgs = codecs.open(file_to_check, 'r', 'utf-8').readlines()
        url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
        results = requests.post(url, data = {'text': 'test', 'desp': msgs})
    except Exception as e:
        print e


    

# set sw=4 ts=4 sts=4 et tw=78
