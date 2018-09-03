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
当一个生成器对象被销毁时，会抛出一个GeneratorExit异常
def myGenerator():  
    try:
        yield 1
    except GeneratorExit:
        print "myGenerator exited"
 
gen = myGenerator()
print gen.next()

GeneratorExit异常只有在生成器对象被激活后，才有可能产生。更确切的说，
需要至少调用一次生成器对象的next方法后，系统才会产生GeneratorExit异常
在上面的示例中，我们都显式地捕获了GeneratorExit异常。如果该异常没有被显式捕获，
生成器对象也不会把该异常向主程序抛出。因为GeneratorExit异常定义的初衷，是方便开发者在生成器对象调用
结束后定义一些收尾的工作，如释放资源等。
'''

'''
生成器对象的close方法
生成器对象的close方法会在生成器对象方法的挂起处抛出一个GeneratorExit异常。
GeneratorExit异常产生后，系统会继续把生成器对象方法后续的代码执行完毕。参见下面的代码。

需要注意的是，GeneratorExit异常的产生意味着生成器对象的生命周期已经结束。
因此，一旦产生了GeneratorExit异常，生成器方法后续执行的语句中，不能再有yield语句，否则会产生RuntimeError
'''

# 协程的定义：协程可以有多个入口点，可以在指定的位置挂起和回复执行
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


# 协程，python3.4中的语法
import asyncio
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

'''
从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。
请注意，async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
    把@asyncio.coroutine替换为async；
    把yield from替换为await。
'''
