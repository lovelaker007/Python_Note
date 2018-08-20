# -*- coding: utf-8 -*-

'''
一个序列对象不必要保存所有的元素。一般来说，一个序列对象至少需要实现如下两个方法。
    __len__方法。该方法返回序列长度，也即序列中元素个数。
    __getitem__方法。该方法有一个整型参数(不妨记为index)。它需要返回序列中下标为index的元素的值。
'''
class MyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
 
    def __len__(self):
        return self.end - self.start
 
    def __getitem__(self, index):
        # 可以处理正负index
        index = index if index >= 0 else index + self.end
        if index < 0 or index >= len(self):
            raise IndexError
        return index + self.start

'''
可迭代对象
iter方法是python的一个内建方法，它会返回一个迭代器对象。它定义如下
iter(o[, sentinel])

第一个参数o可以是一个可迭代对象，也可以是一个可调用对象。
当参数o是可迭代对象时，第二个参数可省。这里又分为两种情况。
    如果参数o实现了__iter__方法，则直接调用该方法，创建迭代器。
    如果参数o没有实现__iter__方法，那么它比是一个序列对象。iter方法根据该序列对象诱导出一个迭代器。
如果参数o是一个可调用对象时，iter方法返回的迭代器工作原理如下。
    每次调用迭代器的next方法时，最终都会调用o方法。此时第2个参数sentinel必须给定。
    当o方法的返回值与sentinel相同时，抛出StopIteration异常。
'''
    
'''
一个迭代器，本质上也是一个序列。它需要实现下面两个方法。
next方法（老版本的Python叫__next__方法）。当第1次调用next方法时，会返回序列的第1个元素；
当第2次调用next方法时，会返回序列的第2个元素；当序列中的元素耗尽，抛出StopIteration异常。
__iter__方法。前面说过__iter__方法通常返回迭代器对象。因此，对于一个迭代器来说，它的__iter__方法只需返回其本身即可。
通过上面的定义，我们知道，一个迭代器对象，也必是可迭代的。
'''
class MyIterator:
    def __init__(self, start, end):
        self.start = start
        self.end = end
 
    def next(self):
        if self.start >= self.end:
            raise StopIteration
        self.start = self.start + 1
        return self.start - 1
 
    def __iter__(self):
        return self
