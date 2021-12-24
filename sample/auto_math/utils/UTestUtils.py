import os
import sys
import time
import unittest

# from sample.auto_math.utils import HTMLTestRunner
from HTMLTestRunner import HTMLTestRunner

class Test3(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("execute setUpClass")

    @classmethod
    def tearDownClass(self):
        print("execute tearDownClass")

    def setUp(self):
        print("execute setUp")

    def tearDown(self):
        print("execute tearDown")

    def test_one(self):
        print('execute test_one')
        self.assertTrue('FOO'.isupper())

    def test_two(self):
        print('execute test_two')


if __name__ == '__main__':
        full_time_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        suite = unittest.TestSuite()
        # Test3是要测试的类名，test_one是要执行的测试方法
        suite.addTest(Test3("test_one"))
        suite.addTest(Test3("test_two"))
        # 实践中发现执行时的当前路径，不一定是此文件所在的文件夹，所以使用绝对路径
        print(f"{os.getcwd()}")
        filename = './result/html/result_%s.html'%full_time_timestamp
        fb = open(filename, 'wb+')
        runner = HTMLTestRunner(stream=fb, title="HTMLTestRunner Report", description="test")
        runner.run(suite)
        fb.close()