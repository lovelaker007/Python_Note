# -*- coding: utf-8 -*-

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def func1():
    os.chdir(r'C:\Users\admin\WWH\python')
    print 'now the working dir is %s' % (os.getcwd(), )
    for i in os.listdir('.'):
        if i.startswith('.'):
            continue
        if os.path.isfile(i):
            print '\t文档：%s' % (os.path.join(os.getcwd(), i))
        if os.path.isdir(i):
            print '\t文件夹：%s' % (os.path.join(os.getcwd(), i))


if __name__ == '__main__':
    func1()
