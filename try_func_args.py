#coding=utf-8

def func1(a, b, *args, c, d='laker', e='if you', **kwargs):
    print(a, b)
    print(args)
    print(c)
    print(d, e)
    print(kwargs)


if __name__ == '__main__':
    func1(1, 2, 3, c=4)
