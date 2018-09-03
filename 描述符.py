#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 描述符实现特性，实例方法，类方法，静态方法
class Foo(object):
    def __init__(self, age, score):
        super(Foo, self).__init__()
        self._age = None
        self._score = None
        self.age = age
        self.score = score 
        
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 18:
            raise ValueError('too young age')
        self._age = value


from weakref import WeakKeyDictionary
class NonNegative(object):
    def __init__(self, default, limit):
        self.default = default
        self.data = WeakKeyDictionary()
        self.limit = limit

    def __get__(self, instance, class_name):
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        if value < self.limit:
            raise ValueError('too small value')
        self.data[instance] = value

class Foo1(object):
    age = NonNegative(20, 18)
    score = NonNegative(70, 60)

    def __init__(self, age, score):
        super(Foo1, self).__init__()
        self.age = age
        self.score = score


class Property(object):
    def __init__(self, get_fun = None, set_fun = None, del_fun = None, doc = None):
        super(Property, self).__init__()
        self.get_fun = get_fun 
        self.set_fun = set_fun        
        self.del_fun = del_fun       
        self.doc = doc

    def __get__(self, obj, objtype):
        if self.get_fun is None:
            raise AttributeError('can not read the attribute')
        print 'in property __get__'
        return self.get_fun(obj)

    def __set__(self, obj, value):
        if self.set_fun is None:
            raise AttributeError('can not set the attribute')
        print 'in property __set__'
        return self.set_fun(obj, value)       

    def __del__(self, obj):
        if self.del_fun is None:
            raise AttributeError('can not del the attribute')
        print 'in property __del__'
        return self.del_fun(obj)          

class Function(object):
    def __init__(self, fun):
        super(Function, self).__init__()
        self.fun = fun 

    def __get__(self, obj, objtype):
        if obj is not None:
            def new_fun(*args):
                return self.fun(obj, *args)
            return new_fun
        else:
            def new_fun(*args):
                return self.fun(*args)
            return new_fun

class ClassFunction(object):
    def __init__(self, fun):
        super(ClassFunction, self).__init__()
        self.fun = fun 

    def __get__(self, obj, objtype):
        if objtype is None:
            objtype = type(obj)

        def new_fun(*args):
            return self.fun(objtype, *args)
        return new_fun

class StaticFunction(object):
    def __init__(self, fun):
        super(StaticFunction, self).__init__()
        self.fun = fun 

    def __get__(self, obj, objtype):
        return self.fun



if __name__ == '__main__':
    class MyClass(object):
        def name_get(self):
            return self._name

        def name_set(self, name):
            self._name = name

        name = Property(name_get, name_set)

        def __init__(self, name):
            super(MyClass, self).__init__()
            self._name = None
            self.name = name

    class Test(object):
        name = 'classwwh'
    
        def __init__(self):
            self.name = 'instancename'

        def sayname_instance(self):
            print self.name

        @classmethod
        def sayname_class(cls):
            print cls.name

    def _sayname_instance(self):
        print self.name

    def _sayname_class(cls):
        print cls.name

    class Test2(object):
        name = 'classwwh'
    
        def __init__(self):
            self.name = 'instancename'

        sayname_instance = Function(_sayname_instance)
        sayname_class = ClassFunction(_sayname_class)

    def method_in_python():
        t = Test()
        t.sayname_instance()
        t.sayname_class()

        Test.sayname_instance(t)
        Test.sayname_class()
            
    def method_in_my():
        t2 = Test2()
        t2.sayname_instance()
        t2.sayname_class()

        Test2.sayname_instance(t2)
        Test2.sayname_class()
        
            
#     m = MyClass('wwh')
    # print m.name
    # method_in_my()


















