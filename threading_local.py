# -*- coding: utf-8 -*-

'''
local = threading.local()创建线程独有对象

创建线程独有对象之后，在全局范围内有效，但是该对象在线程之间相互隔离。
一个线程对该对象的修改，不会影响别的线程
'''

import threading

local = threading.local()

def func1(name):
    # 线程可像全局变量一样使用local，不用担心其他线程
    local.name = name
    func2()

def func2():
    print 'hello %s from %s' % (local.name, threading.current_thread().name)

t1 = threading.Thread(target = func1, args = ('laker1', ), name = 'thread1')
t2 = threading.Thread(target = func1, args = ('laker2', ), name = 'thread2')

t1.start()
t2.start()

t1.join()
t2.join()
