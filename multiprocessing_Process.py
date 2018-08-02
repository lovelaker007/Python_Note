# -*- coding: utf-8 -*-

import multiprocessing
import os
import time
import atexit

'''
Process类像创建线程一样创建进程
multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
    group: 一般为None
    target: 可调用对象, 进程运行时调用此对象
    name: 指定的进程名称, 如果没有指定, 默认为Process-n形式的名称
    args, kwargs: 传递给target的位置参数和关键字参数
    
方法
    start()：开始进程
    join([timeout])
        主调进程阻塞直到被调进程终止或者timeout超时(如果指定了timeout参数)
    daemon，Boolean类型属性
        在调用start前指定，默认情况下为False，从父进程中继承
        注意daemon为True时，并不表示该进程为守护进程。只是表示如果该进程的父进程终止，这个父进程
        所有的daemon为True的子进程也随之终止 
    terminate()
        终止一个进程
        不要轻易使用该方法，如果进程正在使用queue或者还占有一个lock，很容易导致其他进程出现问题
'''

def daemon_func():
    current = multiprocessing.current_process()
    while True:
        print 'child process hello' 
        time.sleep(2)

def try_daemon():
    p = multiprocessing.Process(target = daemon_func)
    # p.daemon = True
    print 'father process creates child process done'
    p.start()
    time.sleep(5)
    print 'father process exits'


if __name__ == '__main__':
    try_daemon()
    '''
    上面调用的结果如下
    father process creates child process done
    child process hello
    child process hello
    child process hello
    father process exits

    如果子进程没有设置daemon为True的话，应该一直运行，但设置之后，父进程终止了，子进程也随之终止
    '''
