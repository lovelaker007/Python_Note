#coding=utf-8

import unittest


'''
    assertEqual(a, b)     a == b      
    assertNotEqual(a, b)     a != b      
    assertTrue(x)     bool(x) is True      
    assertFalse(x)     bool(x) is False      
    assertIsNone(x)     x is None     
    assertIsNotNone(x)     x is not None   
    assertIn(a, b)     a in b    
    assertNotIn(a, b)     a not in b
'''

class MyTest(unittest.TestCase): 
    def tearDown(self):
        # 每个测试用例执行之后做操作
        print('11111')

    def setUp(self):
        # 每个测试用例执行之前做操作
        print('22222')

    @classmethod
    def tearDownClass(self):
    # 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
         print('44444')

    @classmethod
    def setUpClass(self):
    # 必须使用@classmethod 装饰器,所有test运行前运行一次
        print('33333')

    def test_a_run(self):
        # assertEqual表示测试的参数必须相等，否则抛出异常
        self.assertEqual(1, 1)  
        
    def test_b_run(self):
        self.assertEqual(2, 2)  # 测试用例


# mock，对于一个在开发中的函数，可以用mock模拟函数的返回结果

        
if __name__ == '__main__':
    unittest.main()
