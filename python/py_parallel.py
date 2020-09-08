#!/usr/local/bin/python3
#############################################################################
# Script:       py_parallel.py
# Description:  parallel programming 
# Author:       Lu Yi
# Date:         Sep 08 2020
#############################################################################

import sys
import os
import time
import multiprocessing

## I. spawn process with process name
def foo():
    name = multiprocessing.current_process().name
    print ("Starting %s \n" % name)
    time.sleep(3)
    print ("Exiting %s \n" % name)

def spawn_process():
    process_with_name = multiprocessing.Process(name='foo_process', target=foo)

    process_with_name.start()


## spawn process, END

## I. process pool
## apply(), it block until the result is ready
## apply_async(), same as apply but asynchronous
## map(), chops the iterable data
def function_square(data):
    result = data * data
    return result

def process_pool():
    inputs = list(range(100))
    pool = multiprocessing.Pool(processes=5)
    pool_outputs = pool.map(function_square, inputs)
    pool.close()
    pool.join()
    print('Square output (Pool): {}\n'.format(pool_outputs))

## process pool, END

## II. manage state between process
## a manager object controls a server process that holds Python objects and allows other processes to manipylate them
def worker(dict_state, key, item):
    dict_state[key] = item

def manage_state():
    ## manager object, shares between the workers, each worker updates an index
    mgr = multiprocessing.Manager()
    dict_data = mgr.dict()
    jobs = [ multiprocessing.Process(target=worker, args=(dict_data, i, i*2)) for i in range(10) ]

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    print('Results: {}\n'.format(dict_data))

## manage state between process, END

## III. synchronize processes
## synchronize process, END


if __name__ == '__main__':

    spawn_process()

    process_pool()

    manage_state()

    ## open to extend
    ## no open to modify

    ## isinstance(), 
    ## dir() to get object all attribution

    ## getattr(), setattr(), hasattr()

    ## MixIn


    ## class special members: __doc__, __module__, __class__, __init__, __del__, __call__, __dict__, __str__, __slots__
    
    ## user defined class, __iter__, __next__ to implement 'for ... in'
    ## __getitem__ to implement index operation of list
    ## instance call directly __call__
