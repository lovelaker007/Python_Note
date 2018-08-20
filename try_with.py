# -*- coding: utf-8 -*-

'''
与with语句密切相关的一个数据结构，叫做context manager。
一个context manager类，至少需要定义__enter__和__exit__两个方法。

with语句的执行过程：
1.  评估with语句中的context表达式，并创建context manager对象。
(事实上，一个with语句中可以有多个context manager对象，后文再介绍.)
2. 加载context manager的__exit__方法，以备后用。
3. 执行context manager的__enter__方法。
    __enter__方法的返回值会通过with语句传给调用者
    with somestates as o语句就是将__enter__方法的返回值记作a
4. 执行with语句块。
5. 执行context manager的__exit__方法。
    __exit__方法有三个参数，保存with语句在运行过程中的异常信息。其中：
    第1个参数保存异常类型；
    第2个参数保存异常对象的值；
    第3个参数保存异常的traceback信息。
    需要指出的是，只有在with语句块中抛出的异常才会交给__exit__方法处理。
    如果在contextmanager的初始化方法和__enter__方法中抛出的异常，并不会交给__exit__方法处理，
    而是直接向外抛出
'''

class MyContextManager:
 
    def __enter__(self):
        print "Entering my conext manager"
 
    def __exit__(self, exc_t, exc_v, traceback):
        print "Exiting my conext manager"
        print "Exception type:"
        print exc_t
        print "Exception value:"
        print exc_v
        print "Exception traceback:"
        print traceback

