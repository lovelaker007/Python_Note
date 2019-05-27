#coding=utf-8

import asyncio
import time
import random


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


# 两个任务还是串行
async def main1():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")


# 两个任务并行
async def main2():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def main3():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )


async def func1(name, number):
    print('task %s start' % (name, ))
    await asyncio.sleep(random.randint(1, 5))
    print('task %s done' % (name, ))
    return number

async def func2(name, number):
    print('task %s start' % (name, ))
    await asyncio.sleep(random.randint(1, 5))
    print('task %s done' % (name, ))
    raise ValueError('value error')


async def main4():
    # 一组协程并行，result是一个列表，收集结果
    result = await asyncio.gather(func1('task1', 1), func2('task2', 2), func1('task3', 3), return_exceptions=True)
    # 一组协程在执行时，如果某个协程抛出异常
        # 如果执行gather时，指定return_exceptions=False参数(默认情况)
            # 异常会向外抛出，gather调用失败，在抛出异常时，还没有执行完的协程不再执行
            # 抛出异常时执行完的协程，不受影响
        # return_exceptions=True
            # gather调用会捕捉异常，并将异常作为该协程调用的结果
            # 其他协程不受影响，gather调用正常返回
    print(result)


async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print('yay!')

async def main5():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except asyncio.TimeoutError:
        print('timeout!')


# asyncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED)
async def main6():
    task1 = asyncio.create_task(func1('task1', 1))
    task2 = asyncio.create_task(func2('task2', 2))
    task3 = asyncio.create_task(func1('task3', 3))
    task_set = {task1, task2, task3}

    done, pending = await asyncio.wait(task_set, return_when=asyncio.FIRST_EXCEPTION)
    print(done)
    print(pending)



if __name__ == '__main__':
    # asyncio.run(main1())
    # asyncio.run(main2())
    # asyncio.run(main3())
    asyncio.run(main6())
