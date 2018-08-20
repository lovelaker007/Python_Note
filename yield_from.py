# -*- coding: utf-8 -*-

from collections import namedtuple
Result = namedtuple('Result', 'count average')

'''
程序调用流程：
定义了三个函数：子生成器，委派生成器，调用方
程序从调用方开始运行

1. 调用方进入迭代：for key, values in data.items()
2. 对于每队key, values，创建委派生成器: group = grouper(results, key)
    该语句只是创建了委派生成器，委派生成器中的语句还没有开始运行
3. 预激委派生成器next(group)
    再委派生成器中，进入while True循环，执行到results[key] = yield from averager()语句 
    创建averager子生成器，创建后继续执行，直到term = yield语句。向外抛出空值，暂停等待外部的输入
    可以发现，next(group)会一直执行，直到遇到yield
4. 控制返回到调用方，进入for value in values循环，对于每个value，group.send(value)
    此时委派生成器暂停在yield from处，他不对传入的value做处理，直接将value传给了子生成器
    此时子生成器暂停在term = yield处，将传入的value存放到term处，继续向下执行
    运行一个循环后，再次执行term = yield语句，向外抛出空值后，再次暂停等待输入
    可以发现，group.send()方法先传入输入，在执行直到遇到yield
    另外，委派生成器只是连接管道的作用
5. 调用方for value in values迭代完毕，每个值都传到了子生成器参与计算
    调用方执行group.send(None), 子生成器接收到None，跳出while循环，执行return语句，返回Result对象
    生成器执行耗尽，且有返回值，将引发StopIteration异常，且StopIteration.value = Result(count, average)。
    此时委派生成器仍然暂停在yield from语句，该语句捕获StopIteration异常，并将value属性，
    作为yield from表达式的返回值。即写入到results字典一次。
    之后委派生成器执行完毕，会引发StopIteration异常，异常冒泡到调用方中，被捕捉
6. 从调用方的角度，一对key，values的迭代处理完毕，开始下一对的处理


对于yield from的意义，网络上的解释
1. 子生成器产出的值都直接传给委派生成器的调用方（客户端代码）
2. 使用send()方法发给委派生成器的值都直接传给子生成器。如果发送的值是None，那么会调用子生成器的next()方法。
    如果发送的值不是None，那么会调用子生成器的send()方法。
    子生成器在运行的过程中如果引发StopIteration异常，那么委派生成器恢复运行。
    如果引发任何其他异常都会向上冒泡，传给委派生成器。
3. 子生成器退出时，return expr表达式会触发StopIteration(expr)异常。
4. yiled from表达式的值是子生成器终止时传给StopIteration异常的第一个参数。
5. 传入委派生成器的异常，除了GeneratorExit之外都传给子生成器的throw()方法。
    如果调用throw()方法时抛出 StopIteration 异常，委派生成器恢复运行。
    StopIteration之外的异常会向上冒泡。传给委派生成器。
6. 如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器上调用close() 方法，
    那么在子生成器上调用close() 方法，如果他有的话。如果调用close()
    方法导致异常抛出，那么异常会向上冒泡，传给委派生成器；否则，委派生成器抛出 GeneratorExit 异常。


yield from伪代码解释
RESULT = yield from EXPR
# EXPR 可以是任何可迭代对象，因为获取迭代器_i 使用的是iter()函数。
_i = iter(EXPR)
try:
    _y = next(_i) # 2 预激子生成器，结果保存在_y 中，作为第一个产出的值
except StopIteration as _e:
    # 3 如果调用的方法抛出StopIteration异常，获取异常对象的value属性，赋值给_r
    # 补充说明，当迭代器运行完毕，就会自动抛出StopIteration异常
    _r = _e.value
else:
    while 1: # 4 运行这个循环时，委派生成器会阻塞，只能作为调用方和子生成器之间的通道
        try:
            _s = yield _y # 5 产出子生成器当前产出的元素；等待调用方发送值并保存到_s中。

        except GeneratorExit as _e:
        # 6 这一部分是用于关闭委派生成器和子生成器，即调用方调用了close方法
        # 因为子生成器可以是任意可迭代对象，所以可能没有close() 方法。
            try:
                _m = _i.close
            except AttributeError:
                pass
            else:
                _m()
            # 调用完子生成器的close方法之后，异常继续抛出，导致委派生成器也调用close方法
            raise _e

        except BaseException as _e: 
        # 7 这一部分处理调用方通过.throw() 方法传入的异常。
        # 如果子生成器是迭代器，没有throw()方法，这种情况会导致委派生成器抛出异常
            _x = sys.exc_info()
            try:
                # 传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成器的throw()方法。
                _m = _i.throw
            except AttributeError:
                # 子生成器没有throw()方法， 调用throw()方法时抛出AttributeError异常传给委派生成器
                raise _e
            else: # 8
                try:
                    _y = _m(*_x)
                except StopIteration as _e:
                     # 如果调用throw()方法时抛出 StopIteration 异常，委派生成器恢复运行。
                     # StopIteration之外的异常会向上冒泡。传给委派生成器。
                    _r = _e.value
                    break

        else: # 9 如果产出值时没有异常
            try: # 10 尝试让子生成器向前执行
                if _s is None: 
                    # 11. 如果发送的值是None，那么会调用子生成器的 __next__()方法。
                    _y = next(_i)
                else:
                    # 11. 如果发送的值不是None，那么会调用子生成器的send()方法。
                    _y = _i.send(_s)
            except StopIteration as _e: # 12
                # 2. 如果调用的方法抛出StopIteration异常，获取异常对象的value属性，赋值给_r,
                # 退出循环，委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
                _r = _e.value 
                break
RESULT = _r 
#13 返回的结果是 _r 即整个yield from表达式的值

上段代码变量说明:
_i 迭代器（子生成器）
_y 产出的值 （子生成器产出的值）
_r 结果 （最终的结果 即整个yield from表达式的值）
_s 发送的值 （调用方发给委派生成器的值，这个只会传给子生成器）
_e 异常 （异常对象）
我们可以看到在代码的第一个 try 部分 使用 _y = next(_i) 预激了子生成器。这可以看出，上一篇我们使用的用于自动预激的装饰器与yield from 语句不兼容。
'''

# 子生成器
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        # main 函数发送数据到这里 
        print("in averager, before yield")
        term = yield
        if term is None: # 终止条件
            break
        total += term
        count += 1
    average = total/count
    print("in averager, return result")
    # 返回的Result会成为grouper函数中yield from表达式的值
    return Result(count, average) 

# 委派生成器
def grouper(results, key):
    print("in grouper, before yield from averager, key is ", key)
    results[key] = yield from averager()
    print("in grouper, after yield from, key is ", key)

# 调用方
def main(data):
    results = {}
    for key, values in data.items():
        print("\ncreate group")
        group = grouper(results, key)
        print("pre active group")
        next(group) 
        for value in values:
            print("send to %r value %f now"%(group, value))
            group.send(value)
        print("send to %r none"%group)
        try:
            group.send(None)
        except StopIteration: 
            pass
    print("report result: ")
    report(results)

# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group, result.average, unit))

data = {
    'girls;kg':[40, 41, 42, 43, 44, 54],
    'girls;m': [1.5, 1.6, 1.8, 1.5, 1.45, 1.6],
    'boys;kg':[50, 51, 62, 53, 54, 54],
    'boys;m': [1.6, 1.8, 1.8, 1.7, 1.55, 1.6],
}


if __name__ == '__main__':
    main(data) 


'''
结果：

create group
pre active group
in grouper, before yield from averager, key is  girls;kg
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 40.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 41.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 42.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 43.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 44.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 54.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> none
in averager, return result
in grouper, after yield from, key is  girls;kg

create group
pre active group
in grouper, before yield from averager, key is  girls;m
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.500000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.600000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.800000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.500000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.450000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.600000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> none
in averager, return result
in grouper, after yield from, key is  girls;m

create group
pre active group
in grouper, before yield from averager, key is  boys;kg
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 50.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 51.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 62.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 53.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 54.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> value 54.000000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40780> none
in averager, return result
in grouper, after yield from, key is  boys;kg

create group
pre active group
in grouper, before yield from averager, key is  boys;m
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.600000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.800000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.800000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.700000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.550000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> value 1.600000 now
in averager, before yield
send to <generator object grouper at 0x0000015112C40048> none
in averager, return result
in grouper, after yield from, key is  boys;m
report result:
 6 boys  averaging 54.00kg
 6 boys  averaging 1.68m
 6 girls averaging 44.00kg
 6 girls averaging 1.58m

'''


'''

def caller_gene():
    pass

def mid_gene():
    try:
        result = yield from sub_gene()
    except GeneratorExit as e:
        print('get GeneratorExit from sub_gene')
        raise e
    except BaseException as e:
        print('get other Exception from sub_gene') 
        raise e

def sub_gene():
    try:
        for i in range(5):
            r = yield i
            print('get %d from caller' % (r, ))
    except GeneratorExit as e:
        print('get close() call from caller')
        raise e
    except BaseException as e:
        print('get throw() call from caller') 
        raise e

>>> c = mid_gene()
>>> next(c)
0
>>> r = c.send(88)
get 88 from caller
>>> print(r)
1
>>> r = c.send(88)
get 88 from caller
>>> print(r)
2
>>> c.close()
get close() call from caller
get GeneratorExit from sub_gene
'''






