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
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger import logger

class FileCreateHandler(FileSystemEventHandler):
    def __init__(self):
        super(FileCreateHandler, self).__init__()

    # override
    def on_any_event(self, event):
        if event.src_path.endswith('.txt'):
            msgs = codecs.open(event.src_path, 'r', 'utf-8').readlines()
            new_msgs = ''
            for line in msgs:
                new_msgs += line.strip() + '\n\n'

            try:
                url = 'https://sc.ftqq.com/SCU41176Teb7e3a6397425be0f27a72a4c2fcdb885c3e08d2af0f5.send'
                req = requests.post(url, data = {'text': 'Notice', 'desp': new_msgs})
            except Exception as e:
                logger.warning(e)



if __name__ == '__main__':
    path = './result'
    observer = Observer()
    observer.schedule(FileCreateHandler(), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



# set sw=4 ts=4 sts=4 et tw=78
