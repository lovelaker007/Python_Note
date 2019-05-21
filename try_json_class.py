#coding:utf-8

class MyClass():
    _name = 'MyClass'

    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print('hello', self.name)

