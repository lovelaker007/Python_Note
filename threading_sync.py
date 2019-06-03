# -*- coding: utf-8 -*-

import threading
import logging
import time
import random

'''
Event
    wait和set/clear调用
    wait有三种情况：不阻塞，阻塞一段时间，一直阻塞。阻塞一段时间，如果event没有被置位
    wait调用返回False
    event.isSet调用可以无阻塞的返回event的状态
    如果多个线程阻塞等待event，当event被置位时，这些线程都会开始运行

Lock
    等待lock也可以有不阻塞，阻塞一段时间，一直阻塞三种情况
    当lock被释放的时候，只有一个线程获得该lock，其他线程仍然需要等待

Condition
    线程条件变量
    有acquire, release方法，和加锁解锁意义一样
    在acquire之后，还可以运行下面的方法
    wait 释放锁，等待通知，获得通知，获得锁
    notify 通知，注意没有释放锁

Local 线程特有数据
    新建一个local对象l，每个线程都可以在该对象中存取数据。该对象是线程安全的，某个线程的修改不会
    影响到别的线程的特有数据
'''


# 商品
product = None
# 条件变量
con = threading.Condition()


# 生产者方法
def produce():
    global product

    if con.acquire():
        while True:
            if product is None:
                print 'produce...'
                product = 'anything'

                # 通知消费者，商品已经生产
                # 通知的时候，并不会释放持有的锁
                con.notify()

            # 此时才释放持有的锁，并进入等待
            # 进入等待后，只有其他线程调用notify，才将其唤醒
            # 唤醒之后，需要先获取锁，才能继续向后运行
            con.wait()
            time.sleep(2)


# 消费者方法
def consume():
    global product

    if con.acquire():
        while True:
            if product is not None:
                print 'consume...'
                product = None

                # 通知生产者，商品已经没了
                con.notify()

            # 等待通知
            con.wait()
            time.sleep(2)


t1 = threading.Thread(target=produce)
t2 = threading.Thread(target=consume)
t2.start()
t1.start()

