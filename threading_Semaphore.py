# -*- coding: utf-8 -*-

'''
sem内部维护一个计数器，所有的操作不能使计数器值小于0

threading.Semaphore
    创建一个sem时，可以指定初始值

    acquire()：获得sem，将sem的值减1，有可能会阻塞
    release(): 释放sem，将sem加1

下面的实例，建立了一个线程池，最多只有规定数量的线程进入线程池

'''
import threading
import logging
import random
import time

class Poll(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.active = []

    def join(self, name):
        with self.lock:
            self.active.append(name)
            print 'thead%s joind, actives are %s' % (name, self.active)

    def leave(self, name):
        with self.lock:
            self.active.remove(name)
            print 'thead%s leaved, actives are %s' % (name, self.active)

def work_sem(s, p):
    with s:
        name = threading.currentThread().getName()
        p.join(name)
        sleep = random.random()
        time.sleep(sleep)
        p.leave(name)

def try_sem():
    s = threading.Semaphore(3)
    p = Poll()

    for i in range(10):
        t = threading.Thread(target = work_sem, name = str(i), args = (s, p))
        t.start()


if __name__ == '__main__':
    try_sem()
