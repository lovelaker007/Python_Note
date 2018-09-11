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


if __name__ == '__main__':
    print example.__name__, example.__doc__

