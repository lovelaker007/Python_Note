# -*- coding: utf-8 -*-

'''
分布式进程

multiprocessing.managers子模块提供了分布式进程，实现了多台计算机的运算
'''
'''
import random, time, Queue
from multiprocessing.managers import BaseManager

SERVER_IP = '127.0.0.1'

# 创建两个队列
task_queue = Queue.Queue()
result_queue = Queue.Queue()

class Queue_Manager(BaseManager):
    pass

# 将queue注册到manager上，别的机器上的进程，可以通过manager访问queue
# 注册时的第一个参数用于区别注册在manager上的各种不同的对象
Queue_Manager.register('get_task_queue', callable = lambda : task_queue)
Queue_Manager.register('get_result_queue', callable = lambda : result_queue)
# 创建manager对象时，指明绑定的地址和口令，便于其他机器连接
manager = Queue_Manager(address = (SERVER_IP, 8888), authkey = 'laker')
manager.start()

task = manager.get_task_queue()
result = manager.get_result_queue()

# 放任务到task中
for i in range(10):
    n = random.randint(0, 100)
    print('Put task %d...' % n)
    task.put(n)

# 从result队列读取结果:
print('Try get results...')
for i in range(10):
    r = result.get(timeout=10)
    print('Result: %s' % r)

# 关闭:
manager.shutdown()
'''


import random, time, Queue
from multiprocessing.managers import BaseManager

SERVER_IP = '127.0.0.1'

# 发送任务的队列:
task_queue = Queue.Queue()
# 接收结果的队列:
result_queue = Queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=(SERVER_IP, 8888), authkey='laker')
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()
# 放几个任务进去:
for i in range(10):
    n = random.randint(0, 10000)
    print('Put task %d...' % n)
    task.put(n)
# 从result队列读取结果:
print('Try get results...')
for i in range(10):
    r = result.get(timeout=10)
    print('Result: %s' % r)
# 关闭:
manager.shutdown()


