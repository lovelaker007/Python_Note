# -*- coding: utf-8 -*-

import time

'''
初始化生成器j = jump_range(10)
j.next(), 运行代码到jump = yield index暂停，先向外抛出index，然后等待用户输入
j.send(3), 向生成器输入3，3被存储到jump变量，程序继续运行，直到再次遇到yield

j.close(): 手动关闭生成器，后面的调用会抛出StopIteration异常
j.throw(): 向生成器送入一个异常，如果生成器中没有捕捉异常的语句，则继续抛出异常并结束生成器，
'''
def jump_range(up):
    index = jump = 0
    while index < up:
        jump = yield index
        if not jump:
            jump = 1
        index += jump


'''
协程版本的生产者消费者程序

1. 生产者调用c.next()：初始化消费者，消费者运行到yield r向外抛出r(此时r为空值)之后暂停
2. 生产者运行到c.send(n)暂停：向消费者发送n，消费者运行 n = yield r, 将收到的值存放到n中，继续运行
3. 消费者运行一个循环，再次来到yield r，向外抛出r(r为200 OK)，抛出后暂停
4. 生产者此时在r = c.send(n)处暂停，等待消费者的返回，生产者收到消费者的返回，r = '200 OK'
5. 循环运行

协程版本和多线程版本比较：
协程是在一个线程之内，由编程者控制流程的跳转，生产者准备好后，跳转到消费者执行，消费者执行返回结果，
再跳转到生产者，过程中没有全局变量的竞争访问，也不需要锁来保证全局变量的访问安全
'''
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    c.next()
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()




