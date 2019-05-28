# -*- coding: utf-8 -*-

'''
class multiprocessing.Pool([processes[, initializer[, initargs[, maxtasksperchild]]]])
    processes：进程池中的进程数
    initializer：如果不为None，当每个进程开始运行前，会调用initializer，并传入*initargs参数
    maxtasksperchild：子进程完成任务的最大数量
    
    apply(func[, args[, kwds]])
    挑选进程池中的一个进程，运行func，并将args解包后作为参数传入(args是元祖类型)
    调用func时会阻塞，直到调用完成, 就是说，如果进程池要执行多个任务，这些任务是串行执行的

    apply_async(func[, args[, kwds[, callback]]])
    非阻塞的调用形式，立即返回multiprocessing.pool.AsyncResult类对象result
    result.get(timeout)方法从中获取结果，如果超时引发异常
    callback是回调函数，接受result为参数

    map(func, iterable[, chunksize])
    map方法与内置的map函数行为基本一致，itertable参数为可迭代对象
    对于itertable迭代出的每个元素t，就是进程要完成的任务，会发生func(t)调用
    map调用会一直阻塞主调进程，直到所有的任务完成并返回结果

    map_async(func, iterable[, chunksize[, callback]])
    map的非阻塞版本

    imap(func, iterable[, chunksize])
    与map不同的是，imap的返回结果为iter，需要在主进程中主动使用next来驱动子进程的调用。

    imap_unordered(func, iterable[, chunksize])
    同imap一致，只不过其并不保证返回结果与迭代传入的顺序一致。

    close()
    关闭pool，使其不在接受新的任务。所有的任务完成之后，子进程会退出
    terminate()
    立即结束子进程，不管任务是否处理完毕
    join()
    主进程阻塞等待子进程的退出，join方法要在close或terminate之后使用。

multiprocessing.pool.AsyncResult
    get([timeout])
    获得结果，可指定timeout值

    wait([timeout])
    Wait until the result is available or until timeout seconds pass.

    ready()
    Return whether the call has completed.

    successful()
    Return whether the call completed without raising an exception. 
    Will raise AssertionError if the result is not ready.

'''

import multiprocessing
import time
import random
import sys


def calculate(func, args):
    # 将args展开
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
        )

def calculatestar(args):
    return calculate(*args)

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

def f(x):
    return 1.0 / (x-5.0)

def pow3(x):
    return x**3

def noop(x):
    pass

def exce_task():
    time.sleep(random.randint(1,3))
    raise ValueError('error')

def create_pool():
    PROCESSES = 4
    print 'Creating pool with %d processes\n' % PROCESSES
    global pool
    pool = multiprocessing.Pool(PROCESSES)
    print 'pool = %s' % pool

def create_task(add_exception_task=False):
    global TASKS
    TASKS = [(mul, (i, 7)) for i in range(10)] + \
                [(plus, (i, 8)) for i in range(10)]
    
    if add_exception_task:
        TASKS.append((exce_task, ()))
    print 'create tasks done'
    print TASKS


def try_apply():
    print 'try apply'
    a = int(time.time())
    # 阻塞，一直到所有的任务执行完毕
    results = [pool.apply(calculate, t) for t in TASKS]
    b = int(time.time())
    print 'apply return, use time %d' % (b-a, )
    for r in results:
        print '\t', r

def try_apply_async():
    print 'try apply_async'
    results_apply_async = []
    a = int(time.time())
    for t in TASKS:
        # 该调用立即返回，调用有结果之后，调用callback回调函数
        pool.apply_async(calculate, t, callback=results_apply_async.append)
    b = int(time.time())
    print 'apply_async return, use time %d' % (b-a, )

    time.sleep(3)
    for i in results_apply_async:
        print i

# 比较内置函数map，pool.map，pool.imap消耗时间多少
def compare_used_time():
    N = 100000
    print 'def pow3(x): return x**3'

    t = time.time()
    A = map(pow3, xrange(N))
    print '\tmap(pow3, xrange(%d)):\n\t\t%s seconds' % \
          (N, time.time() - t)

    t = time.time()
    B = pool.map(pow3, xrange(N))
    print '\tpool.map(pow3, xrange(%d)):\n\t\t%s seconds' % \
          (N, time.time() - t)

    t = time.time()
    C = list(pool.imap(pow3, xrange(N), chunksize=N//8))
    print '\tlist(pool.imap(pow3, xrange(%d), chunksize=%d)):\n\t\t%s' \
          ' seconds' % (N, N//8, time.time() - t)

    assert A == B == C, (len(A), len(B), len(C))
    print

    L = [None] * 1000000
    print 'def noop(x): pass'
    print 'L = [None] * 1000000'

    t = time.time()
    A = map(noop, L)
    print '\tmap(noop, L):\n\t\t%s seconds' % \
          (time.time() - t)

    t = time.time()
    B = pool.map(noop, L)
    print '\tpool.map(noop, L):\n\t\t%s seconds' % \
          (time.time() - t)

    t = time.time()
    C = list(pool.imap(noop, L, chunksize=len(L)//8))
    print '\tlist(pool.imap(noop, L, chunksize=%d)):\n\t\t%s seconds' % \
          (len(L)//8, time.time() - t)

    assert A == B == C, (len(A), len(B), len(C))
    print

    del A, B, C, L

def try_timeout():
    print 'Testing ApplyResult.get() with timeout:',
    res = pool.apply_async(calculate, TASKS[0])
    while 1:
        sys.stdout.flush()
        try:
            # apply_async立即返回结果对象
            sys.stdout.write('\n\t%s' % res.get(0.02))
            break
        except multiprocessing.TimeoutError:
            sys.stdout.write('.')
    print

    print 'Testing IMapIterator.next() with timeout:',
    it = pool.imap(calculatestar, TASKS)
    while 1:
        sys.stdout.flush()
        try:
            sys.stdout.write('\n\t%s' % it.next(0.02))
        except StopIteration:
            break
        except multiprocessing.TimeoutError:
            sys.stdout.write('.')
    print

def try_callback():
    print 'Testing callback:'
    A = []
    B = [56, 0, 1, 8, 27, 64, 125, 216, 343, 512, 729]

    def callback_apply_async(m):
        sys.stdout.flush()
        sys.stdout.write('%d' % (m, ))
        A.append(m)

    def callback_map_async(m):
        sys.stdout.flush()
        sys.stdout.write('%s' % (m, ))
        A.extend(m)

    # 每个任务返回的结果为一个整数，A.append可以添加到A中
    r = pool.apply_async(mul, (7, 8), callback=callback_apply_async)
    r.wait()
    # 每个任务返回的结果为一个列表，列表中是所有任务的结果，A.extend可以添加到A中
    r = pool.map_async(pow3, range(10), callback=callback_map_async)
    r.wait()

    if A == B:
        print '\tcallbacks succeeded\n'
    else:
        print '\t*** callbacks failed\n\t\t%s != %s\n' % (A, B)



if __name__ == '__main__':
    
    create_pool()
    create_task(add_exception_task=True)

    try_apply_async()
    pool.close()
    pool.join()




