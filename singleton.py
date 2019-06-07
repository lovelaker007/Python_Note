#coding=utf-8


# 装饰器版本
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Singleton1(object):
    pass


# 重写__new__方法
class Singleton2():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton2, cls).__new__(cls, *args, **kwargs)
        return cls._instance


# 改写元类
# 类由type创建，创建类时，type的__init__方法自动执行，
# 调用类()时，执行type的 __call__方法(类的__new__方法,类的__init__方法)
class SingletonType(type):
    # 注意调用__call__时，第一个参数是type类的对象，就是要创建的那个类
    # 因此此处用cls值代替
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance 

class Singleton3(metaclass=SingletonType):
    pass


def try_single(cls):
    a = cls()
    b = cls()
    print("a is b: %s", (a is b, ))


if __name__ == '__main__':
    try_single(Singleton3)

