#!/usr/local/bin/python3
#############################################################################
# Script:       concurrent.py
# Description:  future programming 
# Author:       Yi
# Date:         Mar 11 2021
#############################################################################

import sys
import os
import time
import multiprocessing
import concurrent.futures
import requests


def task(url, timeout=60):
    return requests.get(url, timeout=timeout)


def tpool_run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_tasks = [executor.submit(task, url) for url in URLS]
    
        for f in future_tasks:
## no blocking, just test when loop start
            if f.running():
                print('%s is running' % str(f))
    
        for f in concurrent.futures.as_completed(future_tasks):
            try:
                ret = f.done()
                if ret:
                    f_ret = f.result()
                    print('%s, done, result: %s, %s' % (str(f), f_ret.url, len(f_ret.content)))
            except Exception as e:
                f.cancel()
                print(str(e))



if __name__ == '__main__':

    URLS = ['http://qq.com', 'http://sina.com', 'http://www.baidu.com', ]
    tpool_run()


