# -*- coding: utf-8 -*-
# 在新建类的时候，传递name, parents, attrs参数即可
def upper_attr(class_name, class_parents, class_attrs):
    attrs = [(key, value) for key, value in class_attrs.items() if not key.startswith('__')]
    special_attrs = [(key, value) for key, value in class_attrs.items() if key.startswith('__')]
    upper_attr_dict = dict([(key.upper(), value) for key, value in attrs])
    special_attr_dict = dict(special_attrs)
    upper_attr_dict.update(special_attr_dict)
    return type(class_name, class_parents, upper_attr_dict)

class Upperattr_Metaclass(type):
    def __new__(cls, class_name, class_parents, class_attrs):
        upper_attr = [(key.upper(), value) for key, value in class_attrs.items() \
            if not key.startswith('__')]
        special_attr = [(key, value) for key, value in class_attrs.items() if key.startswith('__')]
        attr_dict = dict(upper_attr)
        attr_dict.update(dict(special_attr))
        return type.__new__(cls, class_name, class_parents, attr_dict)

class Test(object):
    __metaclass__ = Upperattr_Metaclass
    abc = 'if you'
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def test_fun(self):
        pass


if __name__ == '__main__':
    t = Test('wwh', 'if you')
    for key in dir(Test):
        if not key.startswith('__'):
            print key
