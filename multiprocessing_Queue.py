# -*- coding: utf-8 -*-

'''
进程安全的队列
多个进程可以向队列中放入/取出对象，遵循FIFO顺序

multiprocessing.Queue([maxsize])
    qsize(), empty(), full()
    返回队列的大小，是否为空，是否满了，但是在多进程环境下，进程获得这些结果后，可能立即被其他进程
    修改，因此这些结果不可靠

    put(obj[, block[, timeout]]) 向队列中放入对象
    默认情况下block为True, timeout为0
    如果block为False，忽略timeout值，此时如果没有足够的空间放入对象，将会引发Queue.Full异常(注意Full
    异常是在Queue模块中实现的)
    如果block为True，timeout为0，如果当时没有足够的空间，将会一直阻塞
    如果timeout为某个正值，会等待最多timeout时间，超时后引发Full异常

    get([block[, timeout]]) 从队列中获取对象
    block和timeout的解释和上面差不多，不同在引发Queue.empty异常

multiprocessing.JoinableQueue([maxsize])
    Queue的子类，具有额外的task_done和join方法
    task_done()
    从队列中获取元素的进程，告诉队列任务处理完毕。
    如果队列收到的task_done调用比，之前存放的元素多，将会引发异常
    join()
    阻塞主调进程，直到Queue中的任务都处理完毕
'''

import multiprocessing
import random
import time

class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        return '%d * %d = %d' % (self.a, self.b, self.a*self.b)
    
    def __str__(self):
        return '%d * %d' % (self.a, self.b)

def work_for_queue(task_queue, result_queue):
    name = multiprocessing.current_process().name
    while True:
        task = task_queue.get()
        if task is None:
            print '%s exit' % (name, )
            task_queue.task_done()
            break
        print '%s get task: %s' % (name, task)
        result = task()
        time.sleep(random.random())
        task_queue.task_done()
        result_queue.put(result)   

def try_queue():
    task_queue = multiprocessing.JoinableQueue()
    result_queue = multiprocessing.Queue()
    main_name = multiprocessing.current_process().name

    num_process = 4
    p_list = [multiprocessing.Process(target = work_for_queue, args = (task_queue, result_queue)) \
            for m in range(num_process)]
    for p in p_list: 
        p.start()

    num_task = 10
    # 新建自定义类的对象，并放到task_queue中
    for i in range(num_task):
        task = Task(i, i+1)
        task_queue.put(task)
    print '%s create %d tasks done!' % (main_name, num_task)

    # 向task_queue中放入和子进程数量相等的None，表示子进程可以退出了
    for n in range(num_process):
        task_queue.put(None)
    print '%s create %d kill_tasks done!' % (main_name, num_process)

    task_queue.join()
    while num_task:
        print 'Result: %s' % (result_queue.get())
        num_task -= 1


if __name__ == '__main__':
    try_queue()
