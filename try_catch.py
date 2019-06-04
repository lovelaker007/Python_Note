#coding=utf-8

def func1():
    try:
        raise ValueError('value error in try')
    except ValueError as e:
        print('catch ValueError')
    except:
        print('catch Exception')
        raise ValueError('value error in except')
    finally:
        print('in finally')


if __name__ == '__main__':
    func1()
