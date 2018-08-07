# -*- coding: utf-8 -*-

# 定义一个类有__call__方法，这个类生成的实例可以被调用
class A(object):
    def __init__(self, name):
        self.name = name

    # 注意定义的是实例方法
    def __call__(self):
        print 'self.__call__ is running, self.name is %s' % (self.name, )

class B(object):
    def __init__(self, name):
        print 'self.__init__ is running'
        self.name = name

    @classmethod
    def __call__(cls, name):
        print 'Class B.__call__ is running, your name is %s' % (name, )

if __name__ == '__main__':
    a = A('laker')
    # a可以直接被调用
    a()

    B('laker')
    # 该调用仍然是新建对象然后初始化，不会直接调用类方法__call__
