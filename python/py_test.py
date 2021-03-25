#!/usr/local/bin/python3
#############################################################################
# Script:       py_test.py
# Description:  used for test
# Author:       
# Date:         
#############################################################################

import sys
import os
import random
import time
import threading
from concurrent.futures import ProcessPoolExecutor


from HTMLTable import HTMLTable

def gen_html():
    # 标题
    table = HTMLTable(caption='商品销量表')
    
    # 表头行
    table.append_header_rows((
        ('名称',    '销量（件）',    '环比',             ''),
        ('',        '',             '增长量 (件)',      '增长率 (%)'),
    ))

    # 合并单元格
    table[0][0].attr.rowspan = 2
    table[0][1].attr.rowspan = 2
    table[0][2].attr.colspan = 2
    
    # 数据行
    table.append_data_rows((
        ('牛仔裤', 110, 10, 20),
        ('T恤', 20, 20, -9),
        ('Nike鞋', 50, 22, 10),
    ))
    
    # 标题样式
    table.caption.set_style({
        'font-size': '15px',
    })
    
    # 表格样式，即<table>标签样式
    table.set_style({
        'border-collapse': 'collapse',
        'word-break': 'keep-all',
        'white-space': 'nowrap',
        'font-size': '14px',
    })
    
    # 统一设置所有单元格样式，<td>或<th>
    table.set_cell_style({
        'border-color': '#000',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '5px',
    })
    
    # 表头样式
    table.set_header_row_style({
        'color': '#fff',
        'background-color': '#48a6fb',
        'font-size': '18px',
    })
    
    # 覆盖表头单元格字体样式
    table.set_header_cell_style({
        'padding': '15px',
    })
    
    # 调小次表头字体大小
    table[1].set_cell_style({
        'padding': '8px',
        'font-size': '15px',
    })
    
    # 遍历数据行，如果增长量为负，标红背景颜色
    for row in table.iter_data_rows():
        if row[2].value < 0:
            row.set_style({
                'background-color': '#ffdddd',
            })
    
    html = table.to_html()
    print(html)

def fib(n, test_arg):
    if n > 30:
        raise Exception('can not > 30, now %s' % n)
    if n <= 2:
        return 1
    return fib(n-1, test_arg) + fib(n-2, test_arg)

def use_map():
    nums = [random.randint(0, 33) for _ in range(0, 10)]
    with ProcessPoolExecutor() as executor:
        try:
            results = executor.map(fib, nums, nums)
            for num, result in zip(nums, results):
                print('fib(%s) result is %s.' % (num, result))
        except Exception as e:
            print(e)


def action(arg):
    time.sleep(1)
    print ('the arg is:%s\r' %arg)


#方法二：从Thread继承，并重写run()
class MyThread(threading.Thread):
    def __init__(self,arg):
        super(MyThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.arg=arg
    def run(self):#定义每个线程要运行的函数
        time.sleep(1)
        print ('the arg is:%s\r' % self.arg)






if __name__ == '__main__':

    # pass func to Thread
    #for i in range(4):
    #    t = threading.Thread(target=action,args=(i,))
    #    t.start()

    #print ('main thread end!')

    #for i in range(4):
    #    t = MyThread(i)
    #    t.start()

    #print ('main thread end!!')

    # use_map()

    ## terminate_process()
    gen_html()

