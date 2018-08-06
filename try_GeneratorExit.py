def myGenerator():  
    try:
        yield 1
        print "Statement after yield"
    except GeneratorExit:
        print "Generator error caught"
 
    print "End of myGenerator"
 
gen = myGenerator()
print gen.next()
gen.close()
print "End of main caller"

'''
代码执行过程如下：
当调用gen.next方法时，会激活生成器，直至遇到生成器方法的yield语句，返回值1。同时，生成器方法的执行被挂起。
当调用gen.close方法时，恢复生成器方法的执行过程。
系统在yield语句处抛出GeneratorExit异常，执行过程跳到except语句块。
当except语句块处理完毕后，系统会继续往下执行，直至生成器方法执行结束。

代码的输出如下：

1
Generator error caught
End of myGenerator
End of main caller

需要注意的是，GeneratorExit异常的产生意味着生成器对象的生命周期已经结束。
因此，一旦产生了GeneratorExit异常，生成器方法后续执行的语句中，不能再有yield语句，否则会产生RuntimeError
'''
