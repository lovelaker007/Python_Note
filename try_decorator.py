# -*- coding: utf-8 -*-

from functools import wraps   
def my_decorator(func):
    @my_wraps(func)
    def wrapper(*args, **kwargs):
        '''decorator'''
        print('Calling decorated function...')
        return func(*args, **kwargs)
    return wrapper  

# wraps是带有参数的装饰器
def my_wraps(f):
    name = f.__name__
    doc = f.__doc__
    def func1(wrapper):
        wrapper.__name__ = name
        wrapper.__doc__ = doc
        return wrapper
    return func1
 
@my_decorator 
def example():
    """Docstring""" 
    print('Called example function')


# 类装饰器
class Decorator(object):

    def __init__(self, f):
        self.f = f
        self.times = 0

    def __call__(self, *args, **kw):
        self.times += 1
        print('%s called %d times' % (self.f.__name__, self.times))
        return self.f(*args, **kw)


@Decorator
def func1():
    print('if you really want it')


class my_property(object):
    def __init__(self, getter):
        self._getter = getter

    def __get__(self, obj, objtype):
        print('in property __get__')
        self._getter(obj)

    def __set__(self, obj, value):
        print('in property __set__')
        self._setter(obj, value)

    def setter(self, f):
        self._setter = f


class A():

    def __init__(self):
        self._score = 0

    @my_property
    def score(self):
        return self._score

    @score.setter
    def score(self, s):
        self._score = s


if __name__ == '__main__':
    # print example.__name__, example.__doc__
    # for i in range(5):
        # func1()
    a = A()
    a.score = 100
    print(a.score)


