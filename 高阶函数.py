#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 高阶函数
# map：接受两个参数，函数和序列，将函数作用到序列中的每个元素上
# 作用的结果会储存到新建的列表中，并返回

def fun_map(x):
    return x * x

def try_map():
    list_map = range(10)
    list_result = map(fun_map, list_map)
    print 'list_result is list_map: ', list_map is list_result
    print list_result


# reduce: 也是接受一个函数一个序列
# 从序列中取出头两个元素，执行f(l1, l2)，得到结果后和l3一起传入到f中再次计算
# reduce(f, [a, b, c, d]) = f(f(f(a, b), c), d)
# 编写一个str2int函数

def str2int(s):
    def char2int(c):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, \
                '6': 6, '7': 7, '8': 8, '9': 9}[c]
    nums = map(char2int, s)

    def nums2int(num1, num2):
        return 10 * num1 + num2
    return reduce(nums2int, nums)


# filter: 过滤序列
# 过滤之后的元素放到一个新序列，不覆盖原来的序列
def filter_func(i):
    if i % 3 == 0:
        return True
    else:
        return False

def try_filter():
    l = list(range(40))
    filted_l = filter(filter_func, l)
    print 'filted_l is l: %s' % (filted_l is l, )
    print filted_l


# sorted: 对序列排序
# sorter(list_to_be_sort, sort_func)sort_func取出序列中的两个元素，如果
# 计算的结果为-1，排序时元素1在元素2前面；如果为1，在后面
# 单词反方向排序，忽略大小写

def word_sort():
    words = ['bob', 'about', 'Zoo', 'Credit']

    def sort_fun(a, b):
        if a < b:
            return 1
        elif a > b:
            return -1
        return 0
    print sorted(words, sort_fun)


# 函数作为返回值，闭包
# 被返回的函数中的变量在外面的函数中定义
def lazy_sum(*args):
    sum = 0
    def mysum():
        for i in args:
            sum = sum + i
        return sum
    return mysum

def f(x):
    if x < 5:
        return str(x) + 'wwh'
    else:
        return str(x) + 'ifyou'
# print [f(i) for i in range(10)]
# ['0wwh', '1wwh', '2wwh', '3wwh', '4wwh', '5ifyou',
        # '6ifyou', '7ifyou', '8ifyou', '9ifyou']


if __name__ == '__main__':
    # try_map()
    # try_filter()
    word_sort()
